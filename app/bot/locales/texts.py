from typing import Protocol

from app.models import SubscriptionType, UserGender, Currency, SubscriptionPeriod, PackageType


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
    IMAGE_SUCCESS: str

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

    # Package
    GPT3_REQUESTS: str
    GPT3_REQUESTS_DESCRIPTION: str
    GPT4_REQUESTS: str
    GPT4_REQUESTS_DESCRIPTION: str
    THEMATIC_CHATS: str
    THEMATIC_CHATS_DESCRIPTION: str
    DALLE3_REQUESTS: str
    DALLE3_REQUESTS_DESCRIPTION: str
    FACE_SWAP_REQUESTS: str
    FACE_SWAP_REQUESTS_DESCRIPTION: str
    ACCESS_TO_CATALOG: str
    ACCESS_TO_CATALOG_DESCRIPTION: str
    ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES: str
    ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES_DESCRIPTION: str
    FAST_ANSWERS: str
    FAST_ANSWERS_DESCRIPTION: str
    MIN_ERROR: str
    VALUE_ERROR: str
    PACKAGE_SUCCESS: str

    # Catalog
    CATALOG: str
    CATALOG_FORBIDDEN_ERROR: str
    PERSONAL_ASSISTANT: str
    CREATIVE_WRITER: str
    LANGUAGE_TUTOR: str
    TECHNICAL_ADVISOR: str

    # Chats
    SHOW_CHATS: str
    CREATE_CHAT: str
    CREATE_CHAT_FORBIDDEN: str
    TYPE_CHAT_NAME: str
    SWITCH_CHAT: str
    SWITCH_CHAT_FORBIDDEN: str
    DELETE_CHAT: str
    DELETE_CHAT_FORBIDDEN: str
    DELETE_CHAT_SUCCESS: str

    # Face swap
    TELL_ME_YOUR_GENDER: str
    YOUR_GENDER: str
    MALE: str
    FEMALE: str
    SEND_ME_YOUR_PICTURE: str
    CHOOSE_YOUR_PACKAGE: str
    CELEBRITIES: str
    FACE_SWAP_MIN_ERROR: str
    FACE_SWAP_MAX_ERROR: str

    ERROR: str
    BACK: str
    CLOSE: str
    EXIT: str

    @staticmethod
    def profile(subscription_type: SubscriptionType,
                gender: UserGender,
                current_model: str,
                monthly_limits,
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

    # Package
    @staticmethod
    def buy():
        raise NotImplementedError

    @staticmethod
    def choose_min(package_type: PackageType):
        raise NotImplementedError

    # Chats
    @staticmethod
    def chats(current_chat_name: str, total_chats: int, available_to_create_chats: int):
        raise NotImplementedError

    # Face swap
    @staticmethod
    def choose_face_swap_package(name: str, available_images: int, total_images: int, used_images: int) -> str:
        raise NotImplementedError

    @staticmethod
    def face_swap_package_forbidden(available_images: int):
        raise NotImplementedError

    @staticmethod
    def wait_for_another_request(seconds: int) -> str:
        raise NotImplementedError

    @staticmethod
    def processing_request() -> str:
        raise NotImplementedError
