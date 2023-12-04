from typing import Protocol

from app.models import SubscriptionType, UserGender, Currency, SubscriptionPeriod


class Texts(Protocol):
    START: str
    COMMANDS: str

    # Language
    LANGUAGE: str
    CHOOSE_LANGUAGE: str

    # AI
    MODE: str
    INFO: str
    ALREADY_MAKE_REQUEST: str
    READY_FOR_NEW_REQUEST: str

    # Settings
    SETTINGS: str
    SHOW_NAME_OF_THE_CHAT: str
    SHOW_USAGE_QUOTA_IN_MESSAGES: str
    TURN_ON_VOICE_MESSAGES_FROM_RESPONDS: str

    # Subscription
    MONTH_1: str
    MONTHS_3: str
    MONTHS_6: str
    DISCOUNT: str
    NO_DISCOUNT: str
    SUBSCRIPTION_SUCCESS: str

    CLOSE: str

    @staticmethod
    def profile(subscription_type: SubscriptionType,
                gender: UserGender,
                current_model: str,
                additional_usage_quota) -> str:
        raise NotImplementedError

    # Subscription
    @staticmethod
    def subscribe(currency: Currency):
        raise NotImplementedError

    @staticmethod
    def choose_how_many_months_to_subscribe(subscription_type: SubscriptionType):
        raise NotImplementedError

    @staticmethod
    def cycles_subscribe():
        raise NotImplementedError

    @staticmethod
    def confirmation_subscribe(subscription_type: SubscriptionType, subscription_period: SubscriptionPeriod):
        raise NotImplementedError

    @staticmethod
    def wait_for_another_request(seconds: int) -> str:
        raise NotImplementedError

    @staticmethod
    def processing_request() -> str:
        raise NotImplementedError
