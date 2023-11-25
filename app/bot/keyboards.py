from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.locales.main import get_localization
from app.models import Model


def build_language_keyboard(language_code: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="🇺🇸 English", callback_data='language:en'),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data='language:ru')
        ],
        [InlineKeyboardButton(get_localization(language_code).CLOSE, callback_data='language:close')]
    ])


def build_mode_keyboard(language_code: str, model: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text="✉️ ChatGPT 3.5" + (" ✅" if model == Model.GPT3.value else ""),
                callback_data=f'mode:{Model.GPT3.value}'
            ),
        ],
        [InlineKeyboardButton(get_localization(language_code).CLOSE, callback_data='language:close')]
    ])


def build_settings_keyboard(language_code: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text="TODO",
                callback_data=f'mode:TODO'
            ),
        ],
        [InlineKeyboardButton(get_localization(language_code).CLOSE, callback_data='language:close')]
    ])
