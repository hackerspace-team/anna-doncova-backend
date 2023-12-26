from typing import Protocol, TypedDict, Dict

from app.models.common import Currency
from app.models.package import PackageType
from app.models.subscription import SubscriptionType, SubscriptionPeriod, Subscription
from app.models.transaction import TransactionType, ServiceType
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
😇 /create\\_promo\\_code - *Создать промокод*
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

    # Statistics
    STATISTICS_INFO = """
📊 *Статистика на подходе!*

Пора погрузиться в мир цифр и графиков. Выбери период, и я покажу тебе, как наш бот покорял AI-вершины 🚀:
1️⃣ *Статистика за день* - Узнай, что происходило сегодня! Были ли рекорды?
2️⃣ *Статистика за неделю* - Недельная доза данных. Каковы были тренды?
3️⃣ *Статистика за месяц* - Месяц в цифрах. Сколько достижений мы накопили?
4️⃣ *Статистика за всё время* - Взгляд в прошлое. Откуда мы начали и куда пришли?

Выбирай кнопку и вперёд, к знаниям! 🕵️‍♂️🔍
"""

    # AI
    MODE: str
    INFO: str
    ALREADY_MAKE_REQUEST: str
    READY_FOR_NEW_REQUEST: str
    CONTINUE_GENERATING: str
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
    UNSPECIFIED: str
    MALE: str
    FEMALE: str
    SEND_ME_YOUR_PICTURE: str
    CHOOSE_YOUR_PACKAGE: str
    CELEBRITIES: str
    MOVIE_CHARACTERS: str
    PROFESSIONS: str
    SEVEN_WONDERS_OF_THE_ANCIENT_WORLD: str
    FACE_SWAP_MIN_ERROR: str
    FACE_SWAP_MAX_ERROR: str

    ERROR: str
    BACK: str
    CLOSE: str
    EXIT: str

    @staticmethod
    def statistics(period: str,
                   count_all_users: int,
                   count_activated_users: int,
                   count_subscription_users: Dict,
                   count_income_transactions: Dict,
                   count_expense_transactions: Dict,
                   count_income_transactions_total: int,
                   count_expense_transactions_total: int,
                   count_transactions_total: int,
                   count_expense_money: Dict,
                   count_income_money: Dict,
                   count_income_subscriptions_total_money: float,
                   count_income_packages_total_money: float,
                   count_income_total_money: float,
                   count_expense_total_money: float,
                   count_total_money: float,
                   count_chats_usage: Dict) -> str:
        emojis = Subscription.get_emojis()

        return f"""
📈 *Статистика за {period} готова!*

👤 *Пользователи*
1️⃣ *{'Всего пользователей' if period == 'всё время' else 'Новых пользователей'}:* {count_all_users}
2️⃣ *Из них, пользователи, оплатившие хоть раз:* {count_activated_users}
3️⃣ *Из них, пользователи-подписчики:*
    - *{SubscriptionType.FREE}:* {count_subscription_users[SubscriptionType.FREE]}
    - *{SubscriptionType.STANDARD} {emojis[SubscriptionType.STANDARD]}:* {count_subscription_users[SubscriptionType.STANDARD]}
    - *{SubscriptionType.VIP} {emojis[SubscriptionType.VIP]}:* {count_subscription_users[SubscriptionType.VIP]}
    - *{SubscriptionType.PLATINUM} {emojis[SubscriptionType.PLATINUM]}:* {count_subscription_users[SubscriptionType.PLATINUM]}

💰 *Финансы*
4️⃣ *Транзакции:*
    ➖ *{TransactionType.EXPENSE}:* {count_expense_transactions_total}
    - *{ServiceType.GPT3}:* {count_expense_transactions[ServiceType.GPT3]}
    - *{ServiceType.GPT4}:* {count_expense_transactions[ServiceType.GPT4]}
    - *{ServiceType.DALLE3}:* {count_expense_transactions[ServiceType.DALLE3]}
    - *{ServiceType.FACE_SWAP}:* {count_expense_transactions[ServiceType.FACE_SWAP]}
    - *{ServiceType.VOICE_MESSAGES}:* {count_expense_transactions[ServiceType.VOICE_MESSAGES]}

    ➕ *{TransactionType.INCOME}:* {count_income_transactions_total}
    - *{ServiceType.GPT3}:* {count_income_transactions[ServiceType.GPT3]}
    - *{ServiceType.GPT4}:* {count_income_transactions[ServiceType.GPT4]}
    - *{ServiceType.DALLE3}:* {count_income_transactions[ServiceType.DALLE3]}
    - *{ServiceType.FACE_SWAP}:* {count_income_transactions[ServiceType.FACE_SWAP]}
    - *{ServiceType.ADDITIONAL_CHATS}:* {count_income_transactions[ServiceType.ADDITIONAL_CHATS]}
    - *{ServiceType.ACCESS_TO_CATALOG}:* {count_income_transactions[ServiceType.ACCESS_TO_CATALOG]}
    - *{ServiceType.VOICE_MESSAGES}:* {count_income_transactions[ServiceType.VOICE_MESSAGES]}
    - *{ServiceType.FAST_MESSAGES}:* {count_income_transactions[ServiceType.FAST_MESSAGES]}
    - *{ServiceType.STANDARD}:* {count_income_transactions[ServiceType.STANDARD]}
    - *{ServiceType.VIP}:* {count_income_transactions[ServiceType.VIP]}
    - *{ServiceType.PLATINUM}:* {count_income_transactions[ServiceType.PLATINUM]}

    - *Всего:* {count_transactions_total}
5️⃣ *Расходы:*
   - *{ServiceType.GPT3}:* {count_expense_money[ServiceType.GPT3]}$
   - *{ServiceType.GPT4}:* {count_expense_money[ServiceType.GPT4]}$
   - *{ServiceType.DALLE3}:* {count_expense_money[ServiceType.DALLE3]}$
   - *{ServiceType.FACE_SWAP}:* {count_expense_money[ServiceType.FACE_SWAP]}$
   - *{ServiceType.VOICE_MESSAGES}:* {count_expense_money[ServiceType.VOICE_MESSAGES]}$
   - *Всего:* {count_expense_total_money}$
6️⃣ *Доходы:*
    💳 *Подписки:* {count_income_subscriptions_total_money}₽
    - *{ServiceType.STANDARD} {emojis[ServiceType.STANDARD]}:* {count_income_money[ServiceType.STANDARD]}₽
    - *{ServiceType.VIP} {emojis[ServiceType.VIP]}:* {count_income_money[ServiceType.VIP]}₽
    - *{ServiceType.PLATINUM} {emojis[ServiceType.PLATINUM]}:* {count_income_money[ServiceType.PLATINUM]}₽

    💵 *Пакеты:* {count_income_packages_total_money}₽
    - *{ServiceType.GPT3}:* {count_income_money[ServiceType.GPT3]}₽
    - *{ServiceType.GPT4}:* {count_income_money[ServiceType.GPT4]}₽
    - *{ServiceType.DALLE3}:* {count_income_money[ServiceType.DALLE3]}₽
    - *{ServiceType.FACE_SWAP}:* {count_income_money[ServiceType.FACE_SWAP]}₽
    - *{ServiceType.ADDITIONAL_CHATS}:* {count_income_money[ServiceType.ADDITIONAL_CHATS]}₽
    - *{ServiceType.ACCESS_TO_CATALOG}:* {count_income_money[ServiceType.ACCESS_TO_CATALOG]}₽
    - *{ServiceType.VOICE_MESSAGES}:* {count_income_money[ServiceType.VOICE_MESSAGES]}₽
    - *{ServiceType.FAST_MESSAGES}:* {count_income_money[ServiceType.FAST_MESSAGES]}₽

    - *Всего:* {count_income_total_money}₽
7️⃣ *Выручка:* {count_total_money}₽

🔢 *Созданные чаты*
    - *PERSONAL ASSISTANT:* {count_chats_usage['PERSONAL_ASSISTANT']}
    - *TUTOR:* {count_chats_usage['TUTOR']}
    - *LANGUAGE TUTOR:* {count_chats_usage['LANGUAGE_TUTOR']}
    - *TECHNICAL ADVISOR:* {count_chats_usage['TECHNICAL_ADVISOR']}
    - *MARKETER:* {count_chats_usage['MARKETER']}
    - *SMM SPECIALIST:* {count_chats_usage['SMM_SPECIALIST']}
    - *CONTENT SPECIALIST:* {count_chats_usage['CONTENT_SPECIALIST']}
    - *DESIGNER:* {count_chats_usage['DESIGNER']}
    - *SOCIAL MEDIA PRODUCER:* {count_chats_usage['SOCIAL_MEDIA_PRODUCER']}
    - *LIFE COACH:* {count_chats_usage['LIFE_COACH']}
    - *ENTREPRENEUR:* {count_chats_usage['ENTREPRENEUR']}

    - *Всего:* {count_chats_usage['ALL']}

🔍 Это всё, что тебе нужно знать о текущем положении дел. Вперёд, к новым достижениям! 🚀
"""

    @staticmethod
    def profile(subscription_type: SubscriptionType,
                gender: UserGender,
                current_model: str,
                monthly_limits,
                additional_usage_quota) -> str:
        raise NotImplementedError

    # Subscription
    @staticmethod
    def subscribe(currency: Currency) -> str:
        raise NotImplementedError

    @staticmethod
    def choose_how_many_months_to_subscribe(subscription_type: SubscriptionType) -> str:
        raise NotImplementedError

    @staticmethod
    def cycles_subscribe() -> str:
        raise NotImplementedError

    @staticmethod
    def confirmation_subscribe(subscription_type: SubscriptionType, subscription_period: SubscriptionPeriod) -> str:
        raise NotImplementedError

    # Package
    @staticmethod
    def buy() -> str:
        raise NotImplementedError

    @staticmethod
    def choose_min(package_type: PackageType) -> str:
        raise NotImplementedError

    # Chats
    @staticmethod
    def chats(current_chat_name: str, total_chats: int, available_to_create_chats: int) -> str:
        raise NotImplementedError

    # Face swap
    @staticmethod
    def choose_face_swap_package(name: str, available_images: int, total_images: int, used_images: int) -> str:
        raise NotImplementedError

    @staticmethod
    def face_swap_package_forbidden(available_images: int) -> str:
        raise NotImplementedError

    @staticmethod
    def wait_for_another_request(seconds: int) -> str:
        raise NotImplementedError

    @staticmethod
    def processing_request() -> str:
        raise NotImplementedError
