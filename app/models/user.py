from datetime import datetime, timezone
from typing import List

from app.bot.constants import (GPT3_MONTHLY_LIMIT_MESSAGES_FREE,
                               GPT4_MONTHLY_LIMIT_MESSAGES_FREE,
                               DALLE3_MONTHLY_LIMIT_IMAGES_FREE,
                               FACE_SWAP_MONTHLY_LIMIT_IMAGES_FREE,
                               GPT3_MONTHLY_LIMIT_MESSAGES_STANDARD,
                               GPT4_MONTHLY_LIMIT_MESSAGES_STANDARD,
                               DALLE3_MONTHLY_LIMIT_IMAGES_STANDARD,
                               FACE_SWAP_MONTHLY_LIMIT_IMAGES_STANDARD,
                               GPT3_MONTHLY_LIMIT_MESSAGES_VIP,
                               GPT4_MONTHLY_LIMIT_MESSAGES_VIP,
                               DALLE3_MONTHLY_LIMIT_IMAGES_VIP,
                               FACE_SWAP_MONTHLY_LIMIT_IMAGES_VIP,
                               GPT3_MONTHLY_LIMIT_MESSAGES_PLATINUM,
                               GPT4_MONTHLY_LIMIT_MESSAGES_PLATINUM,
                               DALLE3_MONTHLY_LIMIT_IMAGES_PLATINUM,
                               FACE_SWAP_MONTHLY_LIMIT_IMAGES_PLATINUM)
from app.models.common import Currency, Model
from app.models.subscription import SubscriptionType


class UserQuota:
    GPT3 = "gpt3"
    GPT4 = "gpt4"
    DALLE3 = "dalle3"
    FACE_SWAP = "face_swap"
    ADDITIONAL_CHATS = "additional_chats"
    FAST_MESSAGES = "fast_messages"
    VOICE_MESSAGES = "voice_messages"
    ACCESS_TO_CATALOG = "access_to_catalog"


class UserSettings:
    SHOW_NAME_OF_THE_CHAT = 'show_name_of_the_chat'
    SHOW_USAGE_QUOTA = 'show_usage_quota'
    TURN_ON_VOICE_MESSAGES = 'turn_on_voice_messages'


class UserGender:
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    UNSPECIFIED = 'UNSPECIFIED'


class User:
    id: str
    first_name: str
    last_name: str
    username: str
    current_chat_id: str
    telegram_chat_ids: List[str]
    language_code: str
    gender: UserGender
    is_premium: bool
    current_model: str
    currency: Currency
    subscription_type: SubscriptionType
    last_subscription_limit_update: datetime
    monthly_limits: dict
    additional_usage_quota: dict
    settings: dict
    created_at: datetime
    edited_at: datetime

    DEFAULT_ADDITIONAL_USAGE_QUOTA = {
        UserQuota.GPT3: 0,
        UserQuota.GPT4: 0,
        UserQuota.ADDITIONAL_CHATS: 0,
        UserQuota.DALLE3: 0,
        UserQuota.FACE_SWAP: 0,
        UserQuota.FAST_MESSAGES: False,
        UserQuota.VOICE_MESSAGES: False,
        UserQuota.ACCESS_TO_CATALOG: False,
    }

    DEFAULT_SETTINGS = {
        UserSettings.SHOW_NAME_OF_THE_CHAT: False,
        UserSettings.SHOW_USAGE_QUOTA: True,
        UserSettings.TURN_ON_VOICE_MESSAGES: False,
    }

    DEFAULT_MONTHLY_LIMITS = {
        SubscriptionType.FREE: {
            UserQuota.GPT3: GPT3_MONTHLY_LIMIT_MESSAGES_FREE,
            UserQuota.GPT4: GPT4_MONTHLY_LIMIT_MESSAGES_FREE,
            UserQuota.DALLE3: DALLE3_MONTHLY_LIMIT_IMAGES_FREE,
            UserQuota.FACE_SWAP: FACE_SWAP_MONTHLY_LIMIT_IMAGES_FREE,
        },
        SubscriptionType.STANDARD: {
            UserQuota.GPT3: GPT3_MONTHLY_LIMIT_MESSAGES_STANDARD,
            UserQuota.GPT4: GPT4_MONTHLY_LIMIT_MESSAGES_STANDARD,
            UserQuota.DALLE3: DALLE3_MONTHLY_LIMIT_IMAGES_STANDARD,
            UserQuota.FACE_SWAP: FACE_SWAP_MONTHLY_LIMIT_IMAGES_STANDARD,
        },
        SubscriptionType.VIP: {
            UserQuota.GPT3: GPT3_MONTHLY_LIMIT_MESSAGES_VIP,
            UserQuota.GPT4: GPT4_MONTHLY_LIMIT_MESSAGES_VIP,
            UserQuota.DALLE3: DALLE3_MONTHLY_LIMIT_IMAGES_VIP,
            UserQuota.FACE_SWAP: FACE_SWAP_MONTHLY_LIMIT_IMAGES_VIP,
        },
        SubscriptionType.PLATINUM: {
            UserQuota.GPT3: GPT3_MONTHLY_LIMIT_MESSAGES_PLATINUM,
            UserQuota.GPT4: GPT4_MONTHLY_LIMIT_MESSAGES_PLATINUM,
            UserQuota.DALLE3: DALLE3_MONTHLY_LIMIT_IMAGES_PLATINUM,
            UserQuota.FACE_SWAP: FACE_SWAP_MONTHLY_LIMIT_IMAGES_PLATINUM,
        }
    }

    def __init__(self,
                 id: str,
                 first_name: str,
                 last_name: str,
                 username: str,
                 current_chat_id: str,
                 telegram_chat_ids: List[str],
                 gender=UserGender.UNSPECIFIED,
                 language_code="en",
                 is_premium=False,
                 current_model=Model.GPT3,
                 currency=Currency.RUB,
                 subscription_type=SubscriptionType.FREE,
                 last_subscription_limit_update=None,
                 monthly_limits=None,
                 additional_usage_quota=None,
                 settings=None,
                 created_at=None,
                 edited_at=None):
        self.id = str(id)
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.gender = gender
        self.language_code = language_code
        self.is_premium = is_premium
        self.current_model = current_model
        self.currency = currency
        self.subscription_type = subscription_type
        self.current_chat_id = str(current_chat_id)
        self.telegram_chat_ids = [str(telegram_chat_id) for telegram_chat_id in telegram_chat_ids]
        self.monthly_limits = monthly_limits if monthly_limits is not None \
            else self.DEFAULT_MONTHLY_LIMITS[SubscriptionType.FREE]
        self.additional_usage_quota = additional_usage_quota if additional_usage_quota is not None \
            else self.DEFAULT_ADDITIONAL_USAGE_QUOTA
        self.settings = settings if settings is not None else self.DEFAULT_SETTINGS

        current_time = datetime.now(timezone.utc)
        self.last_subscription_limit_update = last_subscription_limit_update \
            if last_subscription_limit_update is not None else current_time
        self.created_at = created_at if created_at is not None else current_time
        self.edited_at = edited_at if edited_at is not None else current_time

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'gender': self.gender,
            'language_code': self.language_code,
            'is_premium': self.is_premium,
            'current_model': self.current_model,
            'currency': self.currency,
            'subscription_type': self.subscription_type,
            'last_subscription_limit_update': self.last_subscription_limit_update,
            'current_chat_id': self.current_chat_id,
            'telegram_chat_ids': self.telegram_chat_ids,
            'monthly_limits': self.monthly_limits,
            'additional_usage_quota': self.additional_usage_quota,
            'settings': self.settings,
            'created_at': self.created_at,
            'edited_at': self.edited_at
        }
