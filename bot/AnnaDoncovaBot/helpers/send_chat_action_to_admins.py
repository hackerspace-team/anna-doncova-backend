import logging

from aiogram.exceptions import TelegramBadRequest
from aiogram import Bot
from telegram import constants

from AnnaDoncovaBot.config import config


async def send_chat_action_to_admins(bot: Bot):
    for chat_id in config.ADMIN_CHAT_IDS:
        try:
            await bot.send_chat_action(chat_id=chat_id, action=constants.ChatAction.TYPING)
        except TelegramBadRequest as error:
            logging.error(error)
