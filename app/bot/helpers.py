from datetime import datetime

from telegram import User as TelegramUser
from google.cloud import firestore

from app.bot.features.chat import write_chat_in_transaction
from app.bot.features.message import write_message_in_transaction
from app.bot.features.subscription import update_subscription_in_transaction, get_subscription
from app.bot.features.user import write_user_in_transaction, get_user, update_user_in_transaction
from app.models import SubscriptionStatus, UserQuota, User


@firestore.async_transactional
async def create_chat_with_first_message(transaction, telegram_user: TelegramUser, telegram_chat_id: str):
    chat = await write_chat_in_transaction(transaction, telegram_chat_id)
    await write_message_in_transaction(transaction, chat.id, "system", "", "You are a helpful assistant.")
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
        "provider_payment_charge_id": provider_payment_charge_id
    })

    user.monthly_limits = User.DEFAULT_MONTHLY_LIMITS[subscription.type]
    await update_user_in_transaction(transaction, user_id, {
        "monthly_limits": user.monthly_limits,
        "last_subscription_limit_update": datetime.now(),
    })
