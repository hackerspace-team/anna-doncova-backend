import math
import os
import tempfile
import uuid
from datetime import datetime, timezone
from typing import List, Optional

import aiohttp
import ffmpeg
from pydub import AudioSegment
from telegram import User as TelegramUser, Message, InputMediaPhoto, Bot, Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from google.cloud import firestore

from AnnaDoncovaBackend.settings import ADMIN_CHAT_IDS
from app.bot.constants import PARSE_MODE
from app.bot.features.chat import write_chat_in_transaction
from app.bot.features.message import write_message_in_transaction
from app.bot.features.package import get_package, update_package_in_transaction
from app.bot.features.subscription import update_subscription_in_transaction, get_subscription
from app.bot.features.transaction import write_transaction
from app.bot.features.user import write_user_in_transaction, get_user, update_user_in_transaction
from app.bot.integrations.openAI import get_response_speech_to_text, get_response_text_to_speech
from app.bot.keyboards import build_gender_keyboard, build_face_swap_choose_keyboard
from app.bot.locales.main import get_localization
from app.firebase import bucket
from app.models.common import Currency
from app.models.package import PackageType, PackageStatus
from app.models.subscription import SubscriptionStatus
from app.models.transaction import TransactionType, ServiceType
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
        "edited_at": datetime.now(timezone.utc)
    })

    user.monthly_limits = User.DEFAULT_MONTHLY_LIMITS[subscription.type]
    user.additional_usage_quota[UserQuota.ACCESS_TO_CATALOG] = True
    user.additional_usage_quota[UserQuota.FAST_MESSAGES] = True
    user.additional_usage_quota[UserQuota.VOICE_MESSAGES] = True
    await update_user_in_transaction(transaction, user_id, {
        "subscription_type": subscription.type,
        "monthly_limits": user.monthly_limits,
        "additional_usage_quota": user.additional_usage_quota,
        "last_subscription_limit_update": datetime.now(timezone.utc),
        "edited_at": datetime.now(timezone.utc),
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
        "edited_at": datetime.now(timezone.utc),
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
        "edited_at": datetime.now(timezone.utc)
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


async def process_voice_message(voice_url: str, user_id: str):
    with tempfile.TemporaryDirectory() as tempdir:
        unique_id = uuid.uuid4()
        ogg_path = os.path.join(tempdir, f"{unique_id}.ogg")
        wav_path = os.path.join(tempdir, f"{unique_id}.wav")

        await download_file(voice_url, ogg_path)

        convert_ogg_to_wav(ogg_path, wav_path)

        audio = AudioSegment.from_file(wav_path)
        audio_file = open(wav_path, "rb")
        text = await get_response_speech_to_text(audio_file)
        audio_file.close()

        total_price = 0.0001 * math.ceil(audio.duration_seconds)
        await write_transaction(user_id=user_id,
                                type=TransactionType.EXPENSE,
                                service=ServiceType.VOICE_MESSAGES,
                                amount=total_price,
                                currency=Currency.USD,
                                quantity=1)

        return text


async def reply_with_voice(update: Update, text: str, user_id: str, reply_markup: Optional[InlineKeyboardMarkup]):
    audio_content = await get_response_text_to_speech(text)

    total_price = 0.000015 * len(text)
    await write_transaction(user_id=user_id,
                            type=TransactionType.EXPENSE,
                            service=ServiceType.VOICE_MESSAGES,
                            amount=total_price,
                            currency=Currency.USD,
                            quantity=1)

    await update.message.reply_voice(voice=audio_content,
                                     reply_markup=reply_markup)
