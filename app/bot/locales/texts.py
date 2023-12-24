from typing import Protocol, TypedDict

from app.models.common import Currency
from app.models.package import PackageType
from app.models.subscription import SubscriptionType, SubscriptionPeriod
from app.models.user import UserGender


class Role(TypedDict):
    name: str
    description: str
    instruction: str


class Texts(Protocol):
    START: str
    COMMANDS: str
    COMMANDS_ADMIN = """
----------

👨‍💻👩‍💻 *Команды для админа*:
📊 /statistics - *Просмотр статистики*.
"""

    # Feedback
    FEEDBACK: str
    FEEDBACK_SUCCESS: str

    # Profile
    CHANGE_PHOTO: str
    CHANGE_GENDER: str

    # Language
    LANGUAGE: str
    CHOOSE_LANGUAGE: str

    # Promo code
    PROMO_CODE_INFO: str
    PROMO_CODE_INFO_ADMIN = """
🔑 *Время создать магию с промокодами!* ✨

Выбери, для чего ты хочешь создать промокод:
🌠 *Подписка* - открой доступ к эксклюзивным функциям и контенту.
🎨 *Пакет* - добавь специальные возможности для использования AI.

Нажми на нужную кнопку и приступим к созданию! 🚀
"""
    PROMO_CODE_SUCCESS: str
    PROMO_CODE_SUCCESS_ADMIN = """
🌟 Вау!

Твой *промокод успешно создан* и готов к путешествию в карманы наших пользователей. 🚀
Этот маленький кодик обязательно принесёт радость кому-то там!

🎉 Поздравляю, ты настоящий волшебник промокодов!
"""
    PROMO_CODE_CHOOSE_SUBSCRIPTION_ADMIN = """
🌟 *Выбираем подписку для промокода!* 🎁

Выбери тип подписки, на который хочешь дать доступ:
- *STANDARD* ⭐
- *VIP* 🔥
- *PLATINUM* 💎

Выбери и нажми, чтобы создать волшебный ключ доступа! ✨
"""
    PROMO_CODE_CHOOSE_PACKAGE_ADMIN = """
TODO
"""
    PROMO_CODE_CHOOSE_NAME_ADMIN = """
🖋️ *Придумай название для промокода* ✨

Сейчас ты как настоящий волшебник, создающий заклинание! ✨🧙‍
Напиши уникальное и запоминающееся название для твоего промокода.

🔠 Используй буквы, цифры, но помни о волшебстве краткости. Не бойся экспериментировать и вдохновлять пользователей!
"""
    PROMO_CODE_CHOOSE_DATE = """
📅 *Время для волшебства!* 🪄

Введи дату, до которой этот промокод будет разносить счастье и удивление!
Помни, нужен формат ДД.ММ.ГГГГ, например, 25.12.2023 - идеально для Рождественского сюрприза! 🎄

Так что вперёд, выбирай дату, когда магия закончится 🌟
"""
    PROMO_CODE_NAME_EXISTS_ERROR = """
🚫 *Ой-ой, такой код уже существует!* 🤖

Как настоящий инноватор, ты создал код, который уже кто-то придумал! Нужно что-то ещё более уникальное. Попробуй снова, ведь в творчестве нет границ!

Покажи свою оригинальность и креативность. Уверен, на этот раз получится!
"""
    PROMO_CODE_DATE_VALUE_ERROR = """
🚫 Упс!

Кажется, дата заблудилась в календаре и не может найти свой формат 📅

Давай попробуем ещё раз, но на этот раз в формате ДД.ММ.ГГГГ, например, 25.12.2023. Точность — залог успеха!
"""
    PROMO_CODE_EXPIRED_ERROR: str
    PROMO_CODE_NOT_FOUND_ERROR: str
    PROMO_CODE_ALREADY_USED_ERROR: str

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

    # Voice
    VOICE_MESSAGES_FORBIDDEN: str

    # Subscription
    MONTH_1: str
    MONTHS_3: str
    MONTHS_6: str
    DISCOUNT: str
    NO_DISCOUNT: str
    SUBSCRIPTION_SUCCESS: str
    SUBSCRIPTION_RESET: str
    SUBSCRIPTION_END: str

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
    PERSONAL_ASSISTANT: Role
    TUTOR: Role
    LANGUAGE_TUTOR: Role
    CREATIVE_WRITER: Role
    TECHNICAL_ADVISOR: Role
    MARKETER: Role
    SMM_SPECIALIST: Role
    CONTENT_SPECIALIST: Role
    DESIGNER: Role
    SOCIAL_MEDIA_PRODUCER: Role
    LIFE_COACH: Role
    ENTREPRENEUR: Role

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
