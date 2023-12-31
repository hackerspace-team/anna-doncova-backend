import nest_asyncio
import asyncio
from dotenv import load_dotenv

from telegram.ext import Application, CommandHandler

from AnnaDoncovaBackend.settings import TELEGRAM_TOKEN
from app.bot.handlers.command_handlers import applications

nest_asyncio.apply()
load_dotenv()


async def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("applications", applications))

    await application.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
