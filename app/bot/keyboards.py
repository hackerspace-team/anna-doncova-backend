from typing import Dict, List

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.locales.main import get_localization
from app.models import (Model,
                        SubscriptionType,
                        SubscriptionPeriod,
                        PackageType,
                        Role,
                        UserSettings,
                        Chat,
                        UserGender,
                        FaceSwapPackageName)


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
                text="📷️ Face Swap" + (" ✅" if model == Model.Face_Swap else ""),
                callback_data=f'mode:{Model.Face_Swap}'
            ),
        ],
        [InlineKeyboardButton(get_localization(language_code).CLOSE, callback_data='mode:close')]
    ])


def build_settings_keyboard(language_code: str, settings: Dict) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=get_localization(language_code).SHOW_NAME_OF_THE_CHAT + (
                    " ✅" if settings[UserSettings.SHOW_NAME_OF_THE_CHAT] else " ❌"),
                callback_data=f'setting:{UserSettings.SHOW_NAME_OF_THE_CHAT}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).SHOW_USAGE_QUOTA_IN_MESSAGES + (
                    " ✅" if settings[UserSettings.SHOW_USAGE_QUOTA] else " ❌"),
                callback_data=f'setting:{UserSettings.SHOW_USAGE_QUOTA}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).TURN_ON_VOICE_MESSAGES_FROM_RESPONDS + (
                    " ✅" if settings[UserSettings.TURN_ON_VOICE_MESSAGES] else " ❌"
                ),
                callback_data=f'setting:{UserSettings.TURN_ON_VOICE_MESSAGES}'
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


def build_packages_keyboard(language_code: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=get_localization(language_code).GPT3_REQUESTS,
                callback_data=f'package:{PackageType.GPT3}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).GPT4_REQUESTS,
                callback_data=f'package:{PackageType.GPT4}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).THEMATIC_CHATS,
                callback_data=f'package:{PackageType.CHAT}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).DALLE3_REQUESTS,
                callback_data=f'package:{PackageType.DALLE3}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).FACE_SWAP_REQUESTS,
                callback_data=f'package:{PackageType.FACE_SWAP}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).ACCESS_TO_CATALOG,
                callback_data=f'package:{PackageType.ACCESS_TO_CATALOG}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES,
                callback_data=f'package:{PackageType.VOICE_MESSAGES}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).FAST_ANSWERS,
                callback_data=f'package:{PackageType.FAST_MESSAGES}'
            ),
        ],
        [InlineKeyboardButton(get_localization(language_code).CLOSE, callback_data='package:close')]
    ])


def build_quantity_of_packages_keyboard(language_code: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(get_localization(language_code).EXIT, callback_data='quantity_of_package:exit')]
    ])


def build_catalog_keyboard(language_code: str, current_role: Role) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=get_localization(language_code).PERSONAL_ASSISTANT + (
                    " ✅" if current_role == Role.PERSONAL_ASSISTANT else " ❌"
                ),
                callback_data=f'catalog:{Role.PERSONAL_ASSISTANT["name"]}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CREATIVE_WRITER + (
                    " ✅" if current_role == Role.CREATIVE_WRITER else " ❌"
                ),
                callback_data=f'catalog:{Role.CREATIVE_WRITER["name"]}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).LANGUAGE_TUTOR + (
                    " ✅" if current_role == Role.LANGUAGE_TUTOR else " ❌"
                ),
                callback_data=f'catalog:{Role.LANGUAGE_TUTOR["name"]}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).TECHNICAL_ADVISOR + (
                    " ✅" if current_role == Role.TECHNICAL_ADVISOR else " ❌"
                ),
                callback_data=f'catalog:{Role.TECHNICAL_ADVISOR["name"]}'
            ),
        ],
        [InlineKeyboardButton(get_localization(language_code).CLOSE, callback_data='catalog:close')]
    ])


def build_chats_keyboard(language_code: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=get_localization(language_code).SHOW_CHATS,
                callback_data=f'chat:show'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CREATE_CHAT,
                callback_data=f'chat:create'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).SWITCH_CHAT,
                callback_data=f'chat:switch'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).DELETE_CHAT,
                callback_data=f'chat:delete'
            )
        ],
        [InlineKeyboardButton(get_localization(language_code).CLOSE, callback_data='chat:close')]
    ])


def build_create_chat_keyboard(language_code: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(get_localization(language_code).EXIT, callback_data='create_chat:exit')]
    ])


def build_switch_chat_keyboard(language_code: str, current_chat_id: str, chats: List[Chat]) -> InlineKeyboardMarkup:
    buttons = []
    for chat in chats:
        buttons.append([
            InlineKeyboardButton(
                text=f"{chat.title}" + (" ✅" if current_chat_id == chat.id else ""),
                callback_data=f"switch_chat:{chat.id}"
            )
        ])
    return InlineKeyboardMarkup([
        buttons,
        [InlineKeyboardButton(get_localization(language_code).CLOSE, callback_data='switch_chat:close')]
    ])


def build_delete_chat_keyboard(language_code: str, current_chat_id: str, chats: List[Chat]) -> InlineKeyboardMarkup:
    buttons = []
    for chat in chats:
        if current_chat_id != chat.id:
            buttons.append([
                InlineKeyboardButton(
                    text=chat.title,
                    callback_data=f"delete_chat:{chat.id}"
                )
            ])
    return InlineKeyboardMarkup([
        buttons,
        [InlineKeyboardButton(get_localization(language_code).CLOSE, callback_data='delete_chat:close')]
    ])


def build_face_swap_gender_keyboard(language_code: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=get_localization(language_code).MALE,
                callback_data=f'face_swap_gender:{UserGender.MALE}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).FEMALE,
                callback_data=f'face_swap_gender:{UserGender.FEMALE}'
            )
        ],
    ])


def build_face_swap_choose_keyboard(language_code: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CELEBRITIES,
                callback_data=f'face_swap_choose:{FaceSwapPackageName.CELEBRITIES["name"]}'
            )
        ],
    ])


def build_face_swap_package_keyboard(language_code: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(get_localization(language_code).BACK, callback_data='face_swap_package:back')],
        [InlineKeyboardButton(get_localization(language_code).EXIT, callback_data='face_swap_package:exit')]
    ])
