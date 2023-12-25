import nest_asyncio
import asyncio
from dotenv import load_dotenv

from telegram.ext import (Application,
                          CommandHandler,
                          MessageHandler,
                          CallbackQueryHandler,
                          PreCheckoutQueryHandler,
                          filters)

from AnnaDoncovaBackend.settings import TELEGRAM_TOKEN
from app.bot.handlers.command_handlers import (start,
                                               commands,
                                               language,
                                               mode,
                                               info,
                                               profile,
                                               settings,
                                               catalog,
                                               subscribe,
                                               buy,
                                               chats,
                                               feedback,
                                               promo_code,
                                               create_promo_code,
                                               statistics)
from app.bot.handlers.job_handlers import reset_monthly_limits
from app.bot.handlers.message_handlers import handle_message, handle_photo, handle_video, handle_voice
from app.bot.handlers.payment_handlers import pre_checkout, successful
from app.bot.handlers.query_handlers import choose_button

nest_asyncio.apply()
load_dotenv()


async def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("commands", commands))
    application.add_handler(CommandHandler("feedback", feedback))

    # Mode
    application.add_handler(CommandHandler("mode", mode))
    application.add_handler(CommandHandler("info", info))

    # Personal
    application.add_handler(CommandHandler("profile", profile))
    application.add_handler(CommandHandler("language", language))
    application.add_handler(CommandHandler("settings", settings))

    # Payments
    application.add_handler(CommandHandler("subscribe", subscribe))
    application.add_handler(CommandHandler("buy", buy))
    application.add_handler(CommandHandler("promo_code", promo_code))
    application.add_handler(CommandHandler("create_promo_code", create_promo_code))
    application.add_handler(PreCheckoutQueryHandler(pre_checkout))
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful))

    # Text AI features
    application.add_handler(CommandHandler("catalog", catalog))
    application.add_handler(CommandHandler("chats", chats))

    # Admin
    application.add_handler(CommandHandler("statistics", statistics))

    # Common
    application.add_handler(CallbackQueryHandler(choose_button))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    job = application.job_queue.run_repeating(reset_monthly_limits, interval=86400, first=0)

    await job.run(application)

    await application.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
