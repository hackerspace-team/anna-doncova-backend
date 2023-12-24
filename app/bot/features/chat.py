from typing import Optional, Dict, List

from app.bot.features.user import get_user
from app.firebase import db
from app.models.chat import Chat


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


async def get_chats_by_user_id(user_id: str) -> List[Chat]:
    chats_query = db.collection('chats').where("user_id", "==", user_id)
    chats = [Chat(**chat.to_dict()) async for chat in chats_query.stream()]

    return chats


async def create_chat_object(user_id: str, telegram_chat_id: str, title="New chat") -> Chat:
    chat_ref = db.collection('chats').document()
    return Chat(id=chat_ref.id, user_id=user_id, telegram_chat_ids=[telegram_chat_id], title=title)


async def write_chat_in_transaction(transaction, user_id: str, telegram_chat_id: str) -> Chat:
    chat = await create_chat_object(user_id, telegram_chat_id)
    transaction.set(db.collection('chats').document(chat.id), chat.to_dict())

    return chat


async def write_chat(user_id: str, telegram_chat_id: str) -> Chat:
    chat = await create_chat_object(user_id, telegram_chat_id)
    await db.collection('chats').document(chat.id).set(chat.to_dict())

    return chat


async def update_chat(chat_id: str, data: Dict):
    chat_ref = db.collection('chats').document(chat_id)
    await chat_ref.update(data)


async def delete_chat(chat_id: str):
    chat_ref = db.collection('chats').document(chat_id)
    await chat_ref.delete()
