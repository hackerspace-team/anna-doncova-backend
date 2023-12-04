from typing import Dict

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.locales.main import get_localization
from app.models import Model, SubscriptionType, SubscriptionPeriod, Currency


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
                text="✉️ ChatGPT 3.5" + (" ✅" if model == Model.GPT3 else ""),
                callback_data=f'mode:{Model.GPT3}'
            ),
            InlineKeyboardButton(
                text="✉️ ChatGPT 4.0" + (" ✅" if model == Model.GPT4 else ""),
                callback_data=f'mode:{Model.GPT4}'
            ),
        ],
        [
            InlineKeyboardButton(
                text="🖼️ DALL-E 3" + (" ✅" if model == Model.DALLE3 else ""),
                callback_data=f'mode:{Model.DALLE3}'
            ),
            InlineKeyboardButton(
                text="📷️ Face Swap" + (" ✅" if model == Model.FaceSwap else ""),
                callback_data=f'mode:{Model.FaceSwap}'
            ),
        ],
        [InlineKeyboardButton(get_localization(language_code).CLOSE, callback_data='mode:close')]
    ])


def build_settings_keyboard(language_code: str, settings: Dict) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=get_localization(language_code).SHOW_NAME_OF_THE_CHAT + (
                    " ✅" if settings['show_name_of_the_chat'] else " ❌"),
                callback_data=f'setting:show_chat'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).SHOW_USAGE_QUOTA_IN_MESSAGES + (
                    " ✅" if settings['show_usage_quota'] else " ❌"),
                callback_data=f'setting:show_usage_quota'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).TURN_ON_VOICE_MESSAGES_FROM_RESPONDS + (
                    " ✅" if settings['turn_on_voice_messages'] else " ❌"
                ),
                callback_data=f'setting:turn_on_voice_messages'
            ),
        ],
        [InlineKeyboardButton(get_localization(language_code).CLOSE, callback_data='setting:close')]
    ])


def build_subscriptions_keyboard(language_code: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=f"{SubscriptionType.STANDARD} ⭐",
                callback_data=f'subscription:{SubscriptionType.STANDARD}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{SubscriptionType.VIP} 🔥",
                callback_data=f'subscription:{SubscriptionType.VIP}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{SubscriptionType.PLATINUM} 💎",
                callback_data=f'subscription:{SubscriptionType.PLATINUM}'
            ),
        ],
        [InlineKeyboardButton(get_localization(language_code).CLOSE, callback_data='subscription:close')]
    ])


def build_period_of_subscription_keyboard(language_code: str,
                                          subscription_type: SubscriptionType) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=f"{get_localization(language_code).MONTH_1} ({get_localization(language_code).NO_DISCOUNT})",
                callback_data=f'period_of_subscription:{SubscriptionPeriod.MONTH1}:{subscription_type}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{get_localization(language_code).MONTHS_3} ({get_localization(language_code).DISCOUNT} 5%)",
                callback_data=f'period_of_subscription:{SubscriptionPeriod.MONTHS3}:{subscription_type}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{get_localization(language_code).MONTHS_6} ({get_localization(language_code).DISCOUNT} 10%)",
                callback_data=f'period_of_subscription:{SubscriptionPeriod.MONTHS6}:{subscription_type}'
            ),
        ],
        [InlineKeyboardButton(get_localization(language_code).CLOSE, callback_data='period_of_subscription:close')]
    ])
