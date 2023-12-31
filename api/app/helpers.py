from telegram import Bot

from AnnaDoncovaBackend.settings import TELEGRAM_TOKEN, ADMIN_CHAT_IDS


async def send_message_to_admins(message: str):
    bot = Bot(token=TELEGRAM_TOKEN)

    for chat_id in ADMIN_CHAT_IDS:
        await bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')
