from telegram import Bot

from AnnaDoncovaBackend.settings import TELEGRAM_TOKEN, CHAT_IDS


async def send_message_to_admins(message):
    bot = Bot(token=TELEGRAM_TOKEN)

    for chat_id in CHAT_IDS:
        await bot.send_message(chat_id=chat_id, text=message)
