from telegram import User as TelegramUser
from google.cloud import firestore

from app.bot.features.chat import write_chat_in_transaction
from app.bot.features.message import write_message_in_transaction
from app.bot.features.user import write_user_in_transaction


@firestore.async_transactional
async def create_chat_with_first_message(transaction, telegram_user: TelegramUser, telegram_chat_id: str):
    chat = await write_chat_in_transaction(transaction, telegram_chat_id)
    await write_message_in_transaction(transaction, chat.id, "system", "", "You are a helpful assistant.")
    await write_user_in_transaction(transaction, telegram_user, chat.id, telegram_chat_id)
