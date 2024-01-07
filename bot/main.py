import logging

import nest_asyncio
import asyncio
from dotenv import load_dotenv
import os
from aiohttp import web

from telegram.ext import Application, CommandHandler
from AnnaDoncovaBot.handlers.command_handlers import applications
from AnnaDoncovaBot.settings import TELEGRAM_TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)

nest_asyncio.apply()
load_dotenv()


async def start_telegram_bot():
    try:
        application = Application.builder().token(TELEGRAM_TOKEN).build()

        application.add_handler(CommandHandler("applications", applications))

        await application.bot.delete_webhook()

        await application.run_polling()
    except Exception as e:
        logger.error(f"Ошибка при запуске Telegram бота: {e}")


async def web_app():
    try:
        app = web.Application()
        app.router.add_get('/', lambda request: web.Response(text="Hello, I'm running!"))

        return app
    except Exception as e:
        logger.error(f"Ошибка при создании веб-приложения: {e}")


async def main():
    try:
        web_server = web.AppRunner(await web_app())
        await web_server.setup()

        site = web.TCPSite(web_server, '0.0.0.0', int(os.environ.get("PORT", 8080)))
        await site.start()

        await start_telegram_bot()
    except Exception as e:
        logger.error(f"Ошибка при запуске основной функции: {e}")


if __name__ == "__main__":
    asyncio.run(main())
