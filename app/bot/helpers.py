import asyncio
import os
import tempfile
import uuid
from datetime import datetime
from typing import List

import aiohttp
import ffmpeg
from telegram import User as TelegramUser, Message, InputMediaPhoto, Bot, Update
from telegram.ext import CallbackContext
from google.cloud import firestore, speech, texttospeech

from AnnaDoncovaBackend.settings import ADMIN_CHAT_IDS
from app.bot.constants import PARSE_MODE
from app.bot.features.chat import write_chat_in_transaction
from app.bot.features.message import write_message_in_transaction
from app.bot.features.package import get_package, update_package_in_transaction
from app.bot.features.subscription import update_subscription_in_transaction, get_subscription
from app.bot.features.user import write_user_in_transaction, get_user, update_user_in_transaction
from app.bot.keyboards import build_gender_keyboard, build_face_swap_choose_keyboard
from app.bot.locales.main import get_localization
from app.firebase import bucket
from app.models.package import PackageType, PackageStatus
from app.models.subscription import SubscriptionStatus
from app.models.user import User, UserQuota, UserGender


@firestore.async_transactional
async def create_user_and_chat(transaction, telegram_user: TelegramUser, telegram_chat_id: str):
    chat = await write_chat_in_transaction(transaction, str(telegram_user.id), telegram_chat_id)
    await write_user_in_transaction(transaction, telegram_user, chat.id, telegram_chat_id)


@firestore.async_transactional
async def create_subscription(transaction,
                              subscription_id: str,
                              user_id: str,
                              provider_payment_charge_id: str):
    user = await get_user(user_id)
    subscription = await get_subscription(subscription_id)

    await update_subscription_in_transaction(transaction, subscription_id, {
        "status": SubscriptionStatus.ACTIVE,
        "provider_payment_charge_id": provider_payment_charge_id,
        "edited_at": datetime.now()
    })

    user.monthly_limits = User.DEFAULT_MONTHLY_LIMITS[subscription.type]
    user.additional_usage_quota[UserQuota.ACCESS_TO_CATALOG] = True
    user.additional_usage_quota[UserQuota.FAST_MESSAGES] = True
    user.additional_usage_quota[UserQuota.VOICE_MESSAGES] = True
    await update_user_in_transaction(transaction, user_id, {
        "subscription_type": subscription.type,
        "monthly_limits": user.monthly_limits,
        "additional_usage_quota": user.additional_usage_quota,
        "last_subscription_limit_update": datetime.now(),
        "edited_at": datetime.now(),
    })


@firestore.async_transactional
async def create_package(transaction,
                         package_id: str,
                         user_id: str,
                         provider_payment_charge_id: str):
    user = await get_user(user_id)
    package = await get_package(package_id)

    await update_package_in_transaction(transaction, package_id, {
        "status": PackageStatus.SUCCESS,
        "provider_payment_charge_id": provider_payment_charge_id,
        "edited_at": datetime.now(),
    })

    if package.type == PackageType.GPT3:
        user.additional_usage_quota[UserQuota.GPT3] += package.quantity
    elif package.type == PackageType.GPT4:
        user.additional_usage_quota[UserQuota.GPT4] += package.quantity
    elif package.type == PackageType.DALLE3:
        user.additional_usage_quota[UserQuota.DALLE3] += package.quantity
    elif package.type == PackageType.FACE_SWAP:
        user.additional_usage_quota[UserQuota.FACE_SWAP] += package.quantity
    elif package.type == PackageType.CHAT:
        user.additional_usage_quota[UserQuota.ADDITIONAL_CHATS] += package.quantity
    elif package.type == PackageType.FAST_MESSAGES:
        user.additional_usage_quota[UserQuota.FAST_MESSAGES] = True
    elif package.type == PackageType.ACCESS_TO_CATALOG:
        user.additional_usage_quota[UserQuota.ACCESS_TO_CATALOG] = True
    elif package.type == PackageType.VOICE_MESSAGES:
        user.additional_usage_quota[UserQuota.VOICE_MESSAGES] = True

    await update_user_in_transaction(transaction, user_id, {
        "additional_usage_quota": user.additional_usage_quota,
        "edited_at": datetime.now()
    })


@firestore.async_transactional
async def create_new_message_and_update_user(transaction, role: str, content: str, user: User, user_quota: UserQuota):
    await write_message_in_transaction(transaction, user.current_chat_id, role, "", content)

    if user.monthly_limits[user_quota] > 0:
        user.monthly_limits[user_quota] -= 1
    elif user.additional_usage_quota[user_quota] > 0:
        user.additional_usage_quota[user_quota] -= 1
    else:
        raise PermissionError

    await update_user_in_transaction(transaction, user.id, {
        "monthly_limits": user.monthly_limits,
        "additional_usage_quota": user.additional_usage_quota,
    })


@firestore.async_transactional
async def create_new_chat(transaction, user: User, telegram_chat_id: str):
    await write_chat_in_transaction(transaction, user.id, telegram_chat_id)
    user.additional_usage_quota[UserQuota.ADDITIONAL_CHATS] -= 1
    await update_user_in_transaction(transaction, user.id, {
        "additional_usage_quota": user.additional_usage_quota,
    })


async def handle_face_swap(message: Message, context: CallbackContext, user: User):
    if user.gender == UserGender.UNSPECIFIED:
        reply_markup = build_gender_keyboard(user.language_code)
        await message.reply_text(text=get_localization(user.language_code).TELL_ME_YOUR_GENDER,
                                 reply_markup=reply_markup,
                                 parse_mode=PARSE_MODE)
    else:
        photo = bucket.blob(f'users/{user.id}.jpeg')
        if photo.exists():
            reply_markup = build_face_swap_choose_keyboard(user.language_code)
            await message.reply_text(text=get_localization(user.language_code).CHOOSE_YOUR_PACKAGE,
                                     reply_markup=reply_markup,
                                     parse_mode=PARSE_MODE)
        else:
            await message.reply_text(text=get_localization(user.language_code).SEND_ME_YOUR_PICTURE,
                                     parse_mode=PARSE_MODE)
            context.user_data['awaiting_photo'] = True


async def send_images(message: Message, images: List[str]):
    for i in range(0, len(images), 10):
        media_group = [InputMediaPhoto(media=img) for img in images[i:i + 10]]
        await message.reply_media_group(media=media_group)

        if len(images) - i == 1:
            await message.reply_photo(photo=images[i])


async def send_message_to_admins(bot: Bot, message: str):
    for chat_id in ADMIN_CHAT_IDS:
        await bot.send_message(chat_id=chat_id, text=message)


async def download_file(url: str, destination: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(destination, 'wb') as f:
                    f.write(await response.read())


def convert_ogg_to_wav(input_path: str, output_path: str):
    ffmpeg.input(input_path).output(output_path).run()


def speech_to_text(file_path: str, language_code: str):
    client = speech.SpeechClient()

    with open(file_path, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        enable_automatic_punctuation=True,
        sample_rate_hertz=48000,
        language_code=language_code
    )

    response = client.recognize(config=config, audio=audio)

    return " ".join([result.alternatives[0].transcript for result in response.results])


async def process_voice_message(voice_url: str, language_code: str):
    with tempfile.TemporaryDirectory() as tempdir:
        unique_id = uuid.uuid4()
        ogg_path = os.path.join(tempdir, f"{unique_id}.ogg")
        wav_path = os.path.join(tempdir, "voice.wav")

        await download_file(voice_url, ogg_path)

        convert_ogg_to_wav(ogg_path, wav_path)

        loop = asyncio.get_event_loop()
        text = await loop.run_in_executor(None, speech_to_text, wav_path, language_code)
        return text


async def text_to_speech(text: str, language_code: str):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.OGG_OPUS
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    return response.audio_content


async def reply_with_voice(update: Update, text: str, language_code: str):
    audio_content = await text_to_speech(text, language_code)
    await update.message.reply_voice(voice=audio_content)
