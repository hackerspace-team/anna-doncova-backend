from typing import Dict, List

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.locales.main import get_localization
from app.models.chat import Chat
from app.models.common import Model
from app.models.face_swap_package import FaceSwapPackageName
from app.models.package import PackageType
from app.models.subscription import SubscriptionType, SubscriptionPeriod
from app.models.user import UserSettings, UserGender


def build_feedback_keyboard(language_code: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(get_localization(language_code).EXIT, callback_data='feedback:exit')]
    ])


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


def build_profile_keyboard(language_code: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CHANGE_PHOTO,
                callback_data=f'profile:change_photo'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CHANGE_GENDER,
                callback_data=f'profile:change_gender'
            ),
        ],
        [InlineKeyboardButton(get_localization(language_code).EXIT, callback_data='profile:exit')]
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


def build_catalog_keyboard(language_code: str, current_role: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=get_localization(language_code).PERSONAL_ASSISTANT['name'] + (
                    " ✅" if current_role == "PERSONAL_ASSISTANT" else " ❌"
                ),
                callback_data=f'catalog:PERSONAL_ASSISTANT'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).TUTOR['name'] + (
                    " ✅" if current_role == "TUTOR" else " ❌"
                ),
                callback_data=f'catalog:TUTOR'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).LANGUAGE_TUTOR['name'] + (
                    " ✅" if current_role == "LANGUAGE_TUTOR" else " ❌"
                ),
                callback_data=f'catalog:LANGUAGE_TUTOR'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CREATIVE_WRITER['name'] + (
                    " ✅" if current_role == "CREATIVE_WRITER" else " ❌"
                ),
                callback_data=f'catalog:CREATIVE_WRITER'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).TECHNICAL_ADVISOR['name'] + (
                    " ✅" if current_role == "TECHNICAL_ADVISOR" else " ❌"
                ),
                callback_data=f'catalog:TECHNICAL_ADVISOR'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).MARKETER['name'] + (
                    " ✅" if current_role == "MARKETER" else " ❌"
                ),
                callback_data=f'catalog:MARKETER'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).SMM_SPECIALIST['name'] + (
                    " ✅" if current_role == "SMM_SPECIALIST" else " ❌"
                ),
                callback_data=f'catalog:SMM_SPECIALIST'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).CONTENT_SPECIALIST['name'] + (
                    " ✅" if current_role == "CONTENT_SPECIALIST" else " ❌"
                ),
                callback_data=f'catalog:CONTENT_SPECIALIST'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).DESIGNER['name'] + (
                    " ✅" if current_role == "DESIGNER" else " ❌"
                ),
                callback_data=f'catalog:DESIGNER'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).SOCIAL_MEDIA_PRODUCER['name'] + (
                    " ✅" if current_role == "SOCIAL_MEDIA_PRODUCER" else " ❌"
                ),
                callback_data=f'catalog:SOCIAL_MEDIA_PRODUCER'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).LIFE_COACH['name'] + (
                    " ✅" if current_role == "LIFE_COACH" else " ❌"
                ),
                callback_data=f'catalog:LIFE_COACH'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).ENTREPRENEUR['name'] + (
                    " ✅" if current_role == "ENTREPRENEUR" else " ❌"
                ),
                callback_data=f'catalog:ENTREPRENEUR'
            )
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


def build_gender_keyboard(language_code: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=get_localization(language_code).MALE,
                callback_data=f'gender:{UserGender.MALE}'
            )
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).FEMALE,
                callback_data=f'gender:{UserGender.FEMALE}'
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


def build_promo_code_keyboard(language_code: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(get_localization(language_code).EXIT, callback_data='promo_code:exit')]
    ])


def build_promo_code_admin_keyboard(language_code: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text="💳 Подписка",
                callback_data=f'promo_code_admin:subscription'
            )
        ],
        [
            InlineKeyboardButton(
                text="💵 Пакет",
                callback_data=f'promo_code_admin:package'
            )
        ],
        [InlineKeyboardButton(get_localization(language_code).EXIT, callback_data='promo_code_admin:exit')]
    ])


def build_promo_code_admin_subscription_keyboard(language_code: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=f"{SubscriptionType.STANDARD} ⭐",
                callback_data=f'promo_code_admin_subscription:{SubscriptionType.STANDARD}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{SubscriptionType.VIP} 🔥",
                callback_data=f'promo_code_admin_subscription:{SubscriptionType.VIP}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{SubscriptionType.PLATINUM} 💎",
                callback_data=f'promo_code_admin_subscription:{SubscriptionType.PLATINUM}'
            ),
        ],
        [InlineKeyboardButton(get_localization(language_code).EXIT, callback_data='promo_code_admin_subscription:exit')]
    ])


def build_promo_code_admin_period_of_subscription_keyboard(language_code: str,
                                                           subscription_type: SubscriptionType) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=f"{get_localization(language_code).MONTH_1}",
                callback_data=f'promo_code_admin_period_of_subscription:{SubscriptionPeriod.MONTH1}:{subscription_type}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{get_localization(language_code).MONTHS_3}",
                callback_data=f'promo_code_admin_period_of_subscription:{SubscriptionPeriod.MONTHS3}:{subscription_type}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{get_localization(language_code).MONTHS_6}",
                callback_data=f'promo_code_admin_period_of_subscription:{SubscriptionPeriod.MONTHS6}:{subscription_type}'
            ),
        ],
        [
            InlineKeyboardButton(
                get_localization(language_code).EXIT,
                callback_data='promo_code_admin_period_of_subscription:exit'
            )
        ]
    ])


def build_promo_code_admin_packages_keyboard(language_code: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=get_localization(language_code).GPT3_REQUESTS,
                callback_data=f'promo_code_admin_package:{PackageType.GPT3}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).GPT4_REQUESTS,
                callback_data=f'promo_code_admin_package:{PackageType.GPT4}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).THEMATIC_CHATS,
                callback_data=f'promo_code_admin_package:{PackageType.CHAT}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).DALLE3_REQUESTS,
                callback_data=f'promo_code_admin_package:{PackageType.DALLE3}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).FACE_SWAP_REQUESTS,
                callback_data=f'promo_code_admin_package:{PackageType.FACE_SWAP}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).ACCESS_TO_CATALOG,
                callback_data=f'promo_code_admin_package:{PackageType.ACCESS_TO_CATALOG}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES,
                callback_data=f'promo_code_admin_package:{PackageType.VOICE_MESSAGES}'
            ),
        ],
        [
            InlineKeyboardButton(
                text=get_localization(language_code).FAST_ANSWERS,
                callback_data=f'promo_code_admin_package:{PackageType.FAST_MESSAGES}'
            ),
        ],
        [InlineKeyboardButton(get_localization(language_code).EXIT, callback_data='promo_code_admin_package:exit')]
    ])


def build_quantity_of_promo_code_admin_packages_keyboard(language_code: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=get_localization(language_code).EXIT,
                callback_data='quantity_of_promo_code_admin_package:exit'
            )
        ]
    ])


def build_promo_code_admin_name_keyboard(language_code: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=get_localization(language_code).EXIT,
                callback_data='promo_code_admin_name:exit'
            )
        ]
    ])


def build_promo_code_admin_date_keyboard(language_code: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=get_localization(language_code).EXIT,
                callback_data='promo_code_admin_date:exit'
            )
        ]
    ])
