from datetime import datetime, timezone
from typing import Optional, Dict, List

from telegram import User as TelegramUser

from app.firebase import db
from app.models.common import Model, Currency
from app.models.subscription import SubscriptionType
from app.models.user import User, UserGender


async def get_user(user_id: str) -> Optional[User]:
    user_ref = db.collection("users").document(user_id)
    user = await user_ref.get()

    if user.exists:
        return User(**user.to_dict())


async def get_users() -> List[User]:
    users = db.collection("users").stream()
    return [User(**user.to_dict()) async for user in users]


def create_user_object(telegram_user: TelegramUser, user_data: Dict, chat_id: str, telegram_chat_id: str) -> User:
    return User(
        id=str(telegram_user.id),
        first_name=telegram_user.first_name,
        last_name=telegram_user.last_name or "",
        username=telegram_user.username,
        current_chat_id=chat_id,
        telegram_chat_ids=[telegram_chat_id],
        gender=user_data.get('gender', UserGender.UNSPECIFIED),
        language_code=telegram_user.language_code,
        is_premium=telegram_user.is_premium or False,
        current_model=user_data.get("current_model", Model.GPT3),
        currency=user_data.get("currency", Currency.RUB),
        subscription_type=user_data.get("subscription_type", SubscriptionType.FREE),
        last_subscription_limit_update=user_data.get("last_subscription_limit_update", datetime.now(timezone.utc)),
        monthly_limits=user_data.get("monthly_limits", User.DEFAULT_MONTHLY_LIMITS[SubscriptionType.FREE]),
        additional_usage_quota=user_data.get("usage_quota", User.DEFAULT_ADDITIONAL_USAGE_QUOTA),
        settings=user_data.get("settings", User.DEFAULT_SETTINGS),
        created_at=user_data.get("created_at", None)
    )


async def write_user_in_transaction(transaction,
                                    telegram_user: TelegramUser,
                                    chat_id: str,
                                    telegram_chat_id: str) -> User:
    user_ref = db.collection('users').document(str(telegram_user.id))
    user_data = (await user_ref.get()).to_dict() or {}

    created_user = create_user_object(telegram_user, user_data, chat_id, telegram_chat_id)

    transaction.set(user_ref, created_user.to_dict())

    return created_user


async def write_user(telegram_user: TelegramUser, chat_id: str, telegram_chat_id: str) -> User:
    user_ref = db.collection('users').document(str(telegram_user.id))
    user_data = (await user_ref.get()).to_dict() or {}

    created_user = create_user_object(telegram_user, user_data, chat_id, telegram_chat_id)

    await user_ref.set(created_user.to_dict())

    return created_user


async def update_user(user_id: str, data: Dict):
    user_ref = db.collection('users').document(user_id)
    await user_ref.update(data)


async def update_user_in_transaction(transaction, user_id: str, data: Dict):
    transaction.update(db.collection('users').document(user_id), data)
