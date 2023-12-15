from datetime import datetime
from typing import List

from telegram import User as TelegramUser, Message, InputMediaPhoto
from telegram.ext import CallbackContext
from google.cloud import firestore

from app.bot.constants import PARSE_MODE
from app.bot.features.chat import write_chat_in_transaction
from app.bot.features.message import write_message_in_transaction
from app.bot.features.package import get_package, update_package_in_transaction
from app.bot.features.subscription import update_subscription_in_transaction, get_subscription
from app.bot.features.user import write_user_in_transaction, get_user, update_user_in_transaction
from app.bot.keyboards import build_face_swap_gender_keyboard, build_face_swap_choose_keyboard
from app.bot.locales.main import get_localization
from app.firebase import bucket
from app.models import SubscriptionStatus, User, PackageStatus, PackageType, UserQuota, UserGender


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
    user.settings['access_to_catalog'] = True
    user.settings['fast_messages'] = True
    await update_user_in_transaction(transaction, user_id, {
        "subscription_type": subscription.type,
        "monthly_limits": user.monthly_limits,
        "settings": user.settings,
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
        user.settings['fast_messages'] = True
    elif package.type == PackageType.ACCESS_TO_CATALOG:
        user.settings['access_to_catalog'] = True

    await update_user_in_transaction(transaction, user_id, {
        "additional_usage_quota": user.additional_usage_quota,
        "settings": user.settings,
        "edited_at": datetime.now()
    })


@firestore.async_transactional
async def create_new_message_and_update_user(transaction, role: str, content: str, user: User, user_quota: UserQuota):
    await write_message_in_transaction(transaction, user.current_chat_id, role, "", content)

    if user.monthly_limits[user_quota] > 0:
        user.monthly_limits[user_quota] -= 1
    else:
        user.additional_usage_quota[user_quota] -= 1

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
        reply_markup = build_face_swap_gender_keyboard(user.language_code)
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
        print(media_group)
        await message.reply_media_group(media=media_group)

        if len(images) - i == 1:
            await message.reply_photo(photo=images[i])
