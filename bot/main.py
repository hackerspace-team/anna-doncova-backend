import logging
import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy

from AnnaDoncovaBot.config import config
from AnnaDoncovaBot.handlers.common_handler import common_router

WEBHOOK_PATH = f"/bot/{config.BOT_TOKEN.get_secret_value()}"
WEBHOOK_URL = config.WEBHOOK_URL + WEBHOOK_PATH

bot = Bot(token=config.BOT_TOKEN.get_secret_value(), parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage(), sm_strategy=FSMStrategy.GLOBAL_USER)


@asynccontextmanager
async def lifespan(app: FastAPI):
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)

    dp.include_router(common_router)
    yield
    await bot.session.close()


app = FastAPI(lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    try:
        telegram_update = types.Update(**update)
        await dp.feed_update(bot=bot, update=telegram_update)
    except Exception as e:
        logging.exception(f"Error in bot_webhook: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=os.getenv('PORT', 8080))
