from datetime import datetime
from typing import Optional, Dict

from telegram import User as TelegramUser

from app.firebase import db
from app.models import User, Model


async def get_user(user_id: str) -> Optional[User]:
    user_ref = db.collection("users").document(user_id)
    user = await user_ref.get()

    if user.exists:
        return User(**user.to_dict())


async def get_users() -> list[User]:
    users = db.collection("users").stream()
    return [User(**user.to_dict()) async for user in users]


def create_user_object(telegram_user: TelegramUser, user_data: Dict, chat_id: str, message_chat_id: str) -> User:
    return User(
        id=telegram_user.id,
        first_name=telegram_user.first_name,
        last_name=telegram_user.last_name or "",
        username=telegram_user.username,
        current_chat_id=chat_id,
        telegram_chat_id=message_chat_id,
        language_code=telegram_user.language_code,
        is_premium=telegram_user.is_premium or False,
        current_model=user_data.get("current_model", Model.GPT3.value),
        daily_limits=user_data.get("daily_limits", User.DEFAULT_DAILY_LIMITS),
        created_at=user_data.get("created_at", datetime.now())
    )


async def write_user_in_transaction(transaction,
                                    telegram_user: TelegramUser,
                                    chat_id: str,
                                    telegram_chat_id: str,
                                    ) -> User:
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
