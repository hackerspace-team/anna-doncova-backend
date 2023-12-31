import nest_asyncio
import asyncio
from dotenv import load_dotenv
import os
from aiohttp import web

from telegram.ext import Application, CommandHandler
from AnnaDoncovaBot.handlers.command_handlers import applications
from AnnaDoncovaBot.settings import TELEGRAM_TOKEN

nest_asyncio.apply()
load_dotenv()


async def start_telegram_bot():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("applications", applications))

    await application.run_polling()


async def web_app():
    app = web.Application()
    app.router.add_get('/', lambda request: web.Response(text="Hello, I'm running!"))
    return app


async def main():
    web_server = web.AppRunner(await web_app())
    await web_server.setup()
    site = web.TCPSite(web_server, '0.0.0.0', int(os.environ.get("PORT", 8080)))
    await site.start()

    await start_telegram_bot()


if __name__ == "__main__":
    asyncio.run(main())
