from typing import Optional

from app.bot.features.user import get_user
from app.firebase import db
from app.models import Chat


async def get_chat(chat_id: str) -> Optional[Chat]:
    chat_ref = db.collection("chats").document(str(chat_id))
    chat = await chat_ref.get()

    if chat.exists:
        return Chat(**chat.to_dict())


async def get_chat_by_user_id(user_id: str) -> Optional[Chat]:
    user = await get_user(user_id)

    if user:
        chat = await get_chat(user.current_chat_id)
        return chat


async def create_chat_object(telegram_chat_id: str, title="New chat") -> Chat:
    chat_ref = db.collection('chats').document()
    return Chat(id=chat_ref.id, telegram_chat_ids=[telegram_chat_id], title=title)


async def write_chat_in_transaction(transaction, telegram_chat_id: str) -> Chat:
    chat = await create_chat_object(telegram_chat_id)
    transaction.set(db.collection('chats').document(chat.id), chat.to_dict())

    return chat


async def write_chat(telegram_chat_id: str) -> Chat:
    chat = await create_chat_object(telegram_chat_id)
    await db.collection('chats').document(chat.id).set(chat.to_dict())

    return chat
