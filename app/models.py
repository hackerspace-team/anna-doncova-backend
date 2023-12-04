import re
from datetime import datetime, timedelta
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


class Model:
    GPT3 = 'gpt-3.5-turbo'
    GPT4 = 'gpt-4-1106-preview'
    DALLE3 = 'dall-e-3'
    FaceSwap = 'face-swap'


class UserQuota:
    GPT3 = "GPT3"
    GPT4 = "GPT4"
    DALLE3 = "DALLE3"
    FACE_SWAP = "FACE_SWAP"
    ADDITIONAL_CHATS = "additional_chats"


class UserSettings:
    SHOW_NAME_OF_THE_CHAT = 'show_name_of_the_chat'
    SHOW_USAGE_QUOTA = 'show_usage_quota'
    TURN_ON_VOICE_MESSAGES = 'turn_on_voice_messages'
    FAST_MESSAGES = 'fast_messages'
    ACCESS_TO_CATALOG = 'access_to_catalog'


class UserGender:
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHER = 'OTHER'
    UNSPECIFIED = 'UNSPECIFIED'


class SubscriptionType:
    FREE = 'FREE'
    STANDARD = 'STANDARD'
    VIP = 'VIP'
    PLATINUM = 'PLATINUM'


class SubscriptionPeriod:
    MONTH1 = 'MONTH_1'
    MONTHS3 = 'MONTHS_3'
    MONTHS6 = 'MONTHS_6'


class SubscriptionStatus:
    ACTIVE = 'ACTIVE'
    WAITING = 'WAITING'
    FINISHED = 'FINISHED'
    ERROR = 'ERROR'


class Currency:
    USD = 'USD'
    EUR = 'EUR'
    RUB = 'RUB'

    SYMBOLS = {
        RUB: '₽',
        USD: '$',
        EUR: '€'
    }


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
    }

    DEFAULT_SETTINGS = {
        UserSettings.SHOW_NAME_OF_THE_CHAT: False,
        UserSettings.SHOW_USAGE_QUOTA: True,
        UserSettings.TURN_ON_VOICE_MESSAGES: False,
        UserSettings.FAST_MESSAGES: False,
        UserSettings.ACCESS_TO_CATALOG: False,
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

        current_time = datetime.now()
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

    @staticmethod
    def get_quotas(subscription_type: SubscriptionType, additional_usage_quota):
        limits = User.DEFAULT_MONTHLY_LIMITS[subscription_type]
        quotas = {service: limits[service] + additional_usage_quota.get(service, 0) for service in limits}
        quotas['additional_chats'] = additional_usage_quota['additional_chats']

        return quotas


class Chat:
    id: str
    telegram_chat_ids: List[str]
    title: str

    def __init__(self, id: str, telegram_chat_ids: List[str], title="New chat", created_at=None, edited_at=None):
        self.id = str(id)
        self.telegram_chat_id = [str(telegram_chat_id) for telegram_chat_id in telegram_chat_ids]
        self.title = title

        current_time = datetime.now()
        self.created_at = created_at if created_at is not None else current_time
        self.edited_at = edited_at if edited_at is not None else current_time

    def to_dict(self):
        return {
            'id': self.id,
            'telegram_chat_id': self.telegram_chat_id,
            'title': self.title,
            'created_at': self.created_at,
            'edited_at': self.edited_at
        }


class Message:
    id: str
    chat_id: str
    sender: str
    sender_id: str
    content: str

    def __init__(self, id: str, chat_id: str, sender: str, sender_id: str, content: str, created_at=None,
                 edited_at=None):
        self.id = str(id)
        self.chat_id = str(chat_id)
        self.sender = sender
        self.sender_id = str(sender_id)
        self.content = content

        current_time = datetime.now()
        self.created_at = created_at if created_at is not None else current_time
        self.edited_at = edited_at if edited_at is not None else current_time

    def to_dict(self):
        return {
            'id': self.id,
            'chat_id': self.chat_id,
            'sender': self.sender,
            'sender_id': self.sender_id,
            'content': self.content,
            'created_at': self.created_at,
            'edited_at': self.edited_at
        }


class Subscription:
    id: str
    user_id: str
    type: SubscriptionType
    period: SubscriptionPeriod
    status: SubscriptionStatus
    currency: Currency
    amount: float
    provider_payment_charge_id: str
    start_date: datetime
    end_date: datetime

    def __init__(self,
                 id: str,
                 user_id: str,
                 type: SubscriptionType,
                 period: SubscriptionPeriod,
                 status: SubscriptionStatus,
                 currency: Currency,
                 amount: float,
                 provider_payment_charge_id="",
                 start_date=None,
                 end_date=None):
        self.id = str(id)
        self.user_id = str(user_id)
        self.type = type
        self.period = period
        self.status = status
        self.currency = currency
        self.amount = amount
        self.provider_payment_charge_id = provider_payment_charge_id

        self.start_date = start_date if start_date is not None else datetime.now()
        if period == SubscriptionPeriod.MONTH1:
            self.end_date = self.start_date + timedelta(days=30)
        elif period == SubscriptionPeriod.MONTHS3:
            self.end_date = self.start_date + timedelta(days=90)
        elif period == SubscriptionPeriod.MONTHS6:
            self.end_date = self.start_date + timedelta(days=180)
        else:
            self.end_date = end_date

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'period': self.period,
            'status': self.status,
            'currency': self.currency,
            'amount': self.amount,
            'provider_payment_charge_id': self.provider_payment_charge_id,
            'start_date': self.start_date,
            'end_date': self.end_date
        }

    @staticmethod
    def get_prices(currency: Currency):
        prices = {
            SubscriptionType.STANDARD: '',
            SubscriptionType.VIP: '',
            SubscriptionType.PLATINUM: ''
        }

        if currency == Currency.RUB:
            prices[SubscriptionType.STANDARD] = '299₽'
            prices[SubscriptionType.VIP] = '999₽'
            prices[SubscriptionType.PLATINUM] = '1 999₽'
        elif currency == Currency.EUR:
            prices[SubscriptionType.STANDARD] = '2.99€'
            prices[SubscriptionType.VIP] = '9.99€'
            prices[SubscriptionType.PLATINUM] = '19.99€'
        else:
            prices[SubscriptionType.STANDARD] = '$2.99'
            prices[SubscriptionType.VIP] = '$9.99'
            prices[SubscriptionType.PLATINUM] = '$19.99'

        return prices

    @staticmethod
    def get_emojis():
        return {
            SubscriptionType.STANDARD: '⭐',
            SubscriptionType.VIP: '🔥',
            SubscriptionType.PLATINUM: '💎'
        }

    @staticmethod
    def get_price(currency: Currency, subscription_type: SubscriptionType, subscription_period: SubscriptionPeriod):
        price_discount = {
            SubscriptionPeriod.MONTH1: 0,
            SubscriptionPeriod.MONTHS3: 5,
            SubscriptionPeriod.MONTHS6: 10
        }
        price_period = {
            SubscriptionPeriod.MONTH1: 1,
            SubscriptionPeriod.MONTHS3: 3,
            SubscriptionPeriod.MONTHS6: 6,
        }
        prices = Subscription.get_prices(currency)
        price_raw = prices[subscription_type]
        price_clear = re.sub(r'[^\d.]', '', price_raw)
        price = float(price_clear) if '.' in price_clear else int(price_clear)
        price_with_period = price * price_period[subscription_period]
        price_with_discount = price_with_period - (price_with_period * (price_discount[subscription_period] / 100.0))

        return int(price_with_discount)


class Order:
    id: str


class OrderDetail:
    id: str
