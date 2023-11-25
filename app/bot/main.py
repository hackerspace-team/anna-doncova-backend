import nest_asyncio
import asyncio
from dotenv import load_dotenv

from telegram.ext import (Application,
                          CommandHandler,
                          MessageHandler,
                          CallbackQueryHandler,
                          filters)

from AnnaDoncovaBackend.settings import TELEGRAM_TOKEN
from app.bot.handlers.command_handlers import start, language, mode, profile
from app.bot.handlers.job_handlers import reset_daily_limits
from app.bot.handlers.message_handlers import handle_message
from app.bot.handlers.query_handlers import choose_button

nest_asyncio.apply()
load_dotenv()


async def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(CommandHandler("language", language))
    application.add_handler(CommandHandler("mode", mode))
    application.add_handler(CallbackQueryHandler(choose_button))

    application.add_handler(CommandHandler("profile", profile))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    job = application.job_queue.run_repeating(reset_daily_limits, interval=86400, first=0)

    await job.run(application)

    await application.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
