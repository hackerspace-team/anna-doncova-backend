from datetime import datetime, timezone, timedelta

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, LabeledPrice
from telegram.ext import CallbackContext

from AnnaDoncovaBackend.settings import YOOKASSA_TOKEN
from app.bot.constants import PARSE_MODE
from app.bot.features.chat import get_chat_by_user_id, update_chat, get_chats_by_user_id, delete_chat, get_chats
from app.bot.features.face_swap_package import get_face_swap_package_by_user_id_and_name, write_face_swap_package
from app.bot.features.transaction import get_transactions
from app.bot.features.user import update_user, get_user, get_users
from app.bot.handlers.message_handlers import handle_chatgpt
from app.bot.handlers.payment_handlers import PaymentType
from app.bot.helpers import handle_face_swap
from app.bot.keyboards import (build_period_of_subscription_keyboard,
                               build_quantity_of_packages_keyboard,
                               build_create_chat_keyboard,
                               build_switch_chat_keyboard,
                               build_delete_chat_keyboard,
                               build_face_swap_package_keyboard,
                               build_face_swap_choose_keyboard,
                               build_promo_code_admin_subscription_keyboard,
                               build_promo_code_admin_period_of_subscription_keyboard,
                               build_promo_code_admin_name_keyboard,
                               build_gender_keyboard)
from app.bot.locales.main import get_localization
from app.firebase import bucket
from app.models.common import Model
from app.models.face_swap_package import FaceSwapPackageName
from app.models.package import Package, PackageType
from app.models.promo_code import PromoCodeType
from app.models.subscription import Subscription, SubscriptionType, SubscriptionPeriod
from app.models.transaction import TransactionType, ServiceType
from app.models.user import UserQuota, UserGender


async def handle_chat_gpt_selection(query: CallbackQuery, action: str, context: CallbackContext):
    user = await get_user(str(query.from_user.id))

    if action == 'continue_generating':
        context.user_data['recognized_text'] = get_localization(user.language_code).CONTINUE_GENERATING
        if user.current_model == Model.GPT3:
            user_quota = UserQuota.GPT3
        elif user.current_model == Model.GPT4:
            user_quota = UserQuota.GPT4
        else:
            raise NotImplemented

        await handle_chatgpt(query, context, user, user_quota)
        await query.edit_message_reply_markup(reply_markup=None)

        context.user_data['recognized_text'] = None


async def handle_feedback_selection(query: CallbackQuery, value: str, context: CallbackContext):
    if value == 'exit':
        context.user_data['awaiting_feedback'] = False
        await query.delete_message()


async def handle_language_selection(query: CallbackQuery, chosen_language: str):
    await update_user(str(query.from_user.id), {"language_code": chosen_language})

    await query.edit_message_text(text=get_localization(chosen_language).CHOOSE_LANGUAGE,
                                  parse_mode=PARSE_MODE)


async def handle_promo_code_selection(query: CallbackQuery, value: str, context: CallbackContext):
    if value == 'exit':
        context.user_data['awaiting_promo_code'] = False

        await query.delete_message()


async def handle_promo_code_admin_selection(query: CallbackQuery, promo_code_type: str):
    user = await get_user(str(query.from_user.id))

    if promo_code_type == 'subscription':
        photo = bucket.blob(f'subscriptions/{user.language_code}_{user.currency}.png')
        photo_data = photo.download_as_string()
        caption = get_localization(user.language_code).PROMO_CODE_CHOOSE_SUBSCRIPTION_ADMIN
        reply_markup = build_promo_code_admin_subscription_keyboard(user.language_code)
        await query.message.reply_photo(photo=photo_data,
                                        caption=caption,
                                        reply_markup=reply_markup,
                                        parse_mode=PARSE_MODE)
    # elif promo_code_type == 'package':
    #     photo = bucket.blob(f'packages/{user.language_code}_{user.currency}.png')
    #     photo_data = photo.download_as_string()
    #     caption = get_localization(user.language_code).PROMO_CODE_CHOOSE_PACKAGE_ADMIN
    #     reply_markup = build_promo_code_admin_packages_keyboard(user.language_code)
    #     await query.message.reply_photo(photo=photo_data,
    #                                     caption=caption,
    #                                     reply_markup=reply_markup,
    #                                     parse_mode=PARSE_MODE)

    await query.delete_message()


async def handle_promo_code_admin_subscription_selection(query: CallbackQuery, subscription_type: SubscriptionType):
    language_code = (await get_user(str(query.from_user.id))).language_code

    message = get_localization(language_code).choose_how_many_months_to_subscribe(subscription_type)
    reply_markup = build_promo_code_admin_period_of_subscription_keyboard(language_code, subscription_type)

    await query.edit_message_caption(caption=message, reply_markup=reply_markup, parse_mode=PARSE_MODE)


async def handle_promo_code_admin_period_of_subscription_selection(query: CallbackQuery,
                                                                   subscription_type: SubscriptionType,
                                                                   subscription_period: SubscriptionPeriod,
                                                                   context: CallbackContext):
    user = await get_user(str(query.from_user.id))

    context.user_data['awaiting_promo_code_name'] = True
    context.user_data['promo_code_type'] = PromoCodeType.SUBSCRIPTION
    context.user_data['promo_code_subscription_type'] = subscription_type
    context.user_data['promo_code_subscription_period'] = subscription_period

    reply_markup = build_promo_code_admin_name_keyboard(user.language_code)

    await query.edit_message_caption(
        caption=get_localization(user.language_code).PROMO_CODE_CHOOSE_NAME_ADMIN,
        reply_markup=reply_markup,
        parse_mode=PARSE_MODE
    )


async def handle_promo_code_admin_name_selection(query: CallbackQuery,
                                                 value: str,
                                                 context: CallbackContext):
    if value == 'exit':
        context.user_data['awaiting_promo_code_name'] = False
        context.user_data['promo_code_type'] = False
        context.user_data['promo_code_subscription_type'] = False
        context.user_data['promo_code_subscription_period'] = False

        await query.delete_message()


async def handle_promo_code_admin_date_selection(query: CallbackQuery,
                                                 value: str,
                                                 context: CallbackContext):
    if value == 'exit':
        context.user_data['awaiting_promo_code_date'] = False
        context.user_data['promo_code_type'] = False
        context.user_data['promo_code_subscription_type'] = False
        context.user_data['promo_code_subscription_period'] = False

        await query.delete_message()


async def handle_statistics_admin_selection(query: CallbackQuery, period: str):
    user = await get_user(str(query.from_user.id))

    current_date = datetime.now(timezone.utc)
    start_date = None
    end_date = None
    if period == "day":
        start_date = current_date
        end_date = current_date
        period = current_date.strftime("%d.%m.%Y")
    elif period == "week":
        start_date = current_date - timedelta(days=current_date.weekday())
        end_date = start_date + timedelta(days=6)
        period = f"{start_date.strftime('%d.%m.%Y')}-{end_date.strftime('%d.%m.%Y')}"
    elif period == "month":
        start_date = current_date.replace(day=1)
        end_date = current_date.replace(day=1) + timedelta(days=32)
        end_date = end_date - timedelta(days=end_date.day)
        period = f"{start_date.strftime('%d.%m.%Y')}-{end_date.strftime('%d.%m.%Y')}"
    else:
        period = "всё время"

    users = await get_users(start_date, end_date)
    transactions = await get_transactions(start_date, end_date)
    chats = await get_chats(start_date, end_date)

    count_subscription_users = {
        SubscriptionType.FREE: 0,
        SubscriptionType.STANDARD: 0,
        SubscriptionType.VIP: 0,
        SubscriptionType.PLATINUM: 0,
    }
    for user in users:
        count_subscription_users[user.subscription_type] += 1

    paid_users = set()
    count_income_transactions = {
        ServiceType.GPT3: 0,
        ServiceType.GPT4: 0,
        ServiceType.DALLE3: 0,
        ServiceType.FACE_SWAP: 0,
        ServiceType.ADDITIONAL_CHATS: 0,
        ServiceType.ACCESS_TO_CATALOG: 0,
        ServiceType.VOICE_MESSAGES: 0,
        ServiceType.FAST_MESSAGES: 0,
        ServiceType.STANDARD: 0,
        ServiceType.VIP: 0,
        ServiceType.PLATINUM: 0,
    }
    count_expense_transactions = {
        ServiceType.GPT3: 0,
        ServiceType.GPT4: 0,
        ServiceType.DALLE3: 0,
        ServiceType.FACE_SWAP: 0,
        ServiceType.VOICE_MESSAGES: 0,
    }
    count_income_transactions_total = 0
    count_expense_transactions_total = 0
    count_transactions_total = 0
    count_income_money = {
        ServiceType.GPT3: 0,
        ServiceType.GPT4: 0,
        ServiceType.DALLE3: 0,
        ServiceType.FACE_SWAP: 0,
        ServiceType.ADDITIONAL_CHATS: 0,
        ServiceType.ACCESS_TO_CATALOG: 0,
        ServiceType.VOICE_MESSAGES: 0,
        ServiceType.FAST_MESSAGES: 0,
        ServiceType.STANDARD: 0,
        ServiceType.VIP: 0,
        ServiceType.PLATINUM: 0,
    }
    count_expense_money = {
        ServiceType.GPT3: 0,
        ServiceType.GPT4: 0,
        ServiceType.DALLE3: 0,
        ServiceType.FACE_SWAP: 0,
        ServiceType.VOICE_MESSAGES: 0,
    }
    count_income_subscriptions_total_money = 0
    count_income_packages_total_money = 0
    count_expense_total_money = 0
    for transaction in transactions:
        if transaction.type == TransactionType.INCOME:
            count_income_transactions_total += 1
            count_income_transactions[transaction.service] += transaction.quantity
            count_income_money[transaction.service] += transaction.amount
            if (
                transaction.service == ServiceType.STANDARD or
                transaction.service == ServiceType.VIP or
                transaction.service == ServiceType.PLATINUM
            ):
                count_income_subscriptions_total_money += transaction.amount
            else:
                count_income_packages_total_money += transaction.amount
        elif transaction.type == TransactionType.EXPENSE:
            count_expense_transactions_total += 1
            count_expense_transactions[transaction.service] += transaction.quantity
            count_expense_money[transaction.service] += transaction.amount
            count_expense_total_money += transaction.amount
            paid_users.add(transaction.user_id)

        count_transactions_total += 1

    count_all_users = len(users)
    count_activated_users = len(paid_users)
    count_income_total_money = count_income_subscriptions_total_money + count_income_packages_total_money
    total_money = count_income_total_money - count_expense_total_money * 100

    count_chats_usage = {
        'PERSONAL_ASSISTANT': 0,
        'TUTOR': 0,
        'LANGUAGE_TUTOR': 0,
        'TECHNICAL_ADVISOR': 0,
        'MARKETER': 0,
        'SMM_SPECIALIST': 0,
        'CONTENT_SPECIALIST': 0,
        'DESIGNER': 0,
        'SOCIAL_MEDIA_PRODUCER': 0,
        'LIFE_COACH': 0,
        'ENTREPRENEUR': 0,
        'ALL': len(chats),
    }
    for chat in chats:
        count_chats_usage[chat.role] += 1

    await query.message.reply_text(text=get_localization(user.language_code).statistics(
        period=period,
        count_all_users=count_all_users,
        count_activated_users=count_activated_users,
        count_subscription_users=count_subscription_users,
        count_income_transactions=count_income_transactions,
        count_expense_transactions=count_expense_transactions,
        count_income_transactions_total=count_income_transactions_total,
        count_expense_transactions_total=count_expense_transactions_total,
        count_transactions_total=count_transactions_total,
        count_expense_money=count_expense_money,
        count_income_money=count_income_money,
        count_income_subscriptions_total_money=count_income_subscriptions_total_money,
        count_income_packages_total_money=count_income_packages_total_money,
        count_income_total_money=count_income_total_money,
        count_expense_total_money=count_expense_total_money,
        count_total_money=total_money,
        count_chats_usage=count_chats_usage,
    ),
        parse_mode=PARSE_MODE)


async def handle_mode_selection(query: CallbackQuery, mode: str, context: CallbackContext):
    keyboard = query.message.reply_markup.inline_keyboard
    keyboard_changed = False

    new_keyboard = []
    for row in keyboard:
        new_row = []
        for button in row:
            text = button.text
            callback_data = button.callback_data.split(":", 1)[1]

            if callback_data == mode:
                if "✅" not in text:
                    text += " ✅"
                    keyboard_changed = True
            else:
                text = text.replace(" ✅", "")
            new_row.append(InlineKeyboardButton(text, callback_data=button.callback_data))
        new_keyboard.append(new_row)

    if keyboard_changed:
        await update_user(str(query.from_user.id), {"current_model": mode})
        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(new_keyboard))

    if mode == Model.FACE_SWAP:
        user = await get_user(str(query.from_user.id))

        await handle_face_swap(query.message, context, user)


async def handle_profile_selection(query: CallbackQuery, action: str, context: CallbackContext):
    user = await get_user(str(query.from_user.id))

    if action == 'exit':
        context.user_data['awaiting_photo'] = False

        await query.delete_message()
    elif action == 'change_photo':
        await query.message.reply_text(text=get_localization(user.language_code).SEND_ME_YOUR_PICTURE,
                                       parse_mode=PARSE_MODE)
        context.user_data['awaiting_photo'] = True
    elif action == 'change_gender':
        reply_markup = build_gender_keyboard(user.language_code)
        await query.message.reply_text(text=get_localization(user.language_code).TELL_ME_YOUR_GENDER,
                                       reply_markup=reply_markup,
                                       parse_mode=PARSE_MODE)


async def handle_setting_selection(query: CallbackQuery, setting: str):
    user = await get_user(str(query.from_user.id))
    user.settings[setting] = not user.settings[setting]

    keyboard = query.message.reply_markup.inline_keyboard

    new_keyboard = []
    for row in keyboard:
        new_row = []
        for button in row:
            text = button.text
            callback_data = button.callback_data.split(":", 1)[1]

            if callback_data == setting:
                if "✅" in text:
                    text = text.replace(" ✅", " ❌")
                else:
                    text = text.replace(" ❌", " ✅")
            new_row.append(InlineKeyboardButton(text, callback_data=button.callback_data))
        new_keyboard.append(new_row)

    await update_user(str(query.from_user.id), {"settings": user.settings})
    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(new_keyboard))


async def handle_subscription_selection(query: CallbackQuery, subscription_type: SubscriptionType):
    language_code = (await get_user(str(query.from_user.id))).language_code

    message = get_localization(language_code).choose_how_many_months_to_subscribe(subscription_type)
    reply_markup = build_period_of_subscription_keyboard(language_code, subscription_type)

    await query.edit_message_caption(caption=message, reply_markup=reply_markup, parse_mode=PARSE_MODE)


async def handle_period_of_subscription_selection(query: CallbackQuery,
                                                  subscription_type: SubscriptionType,
                                                  subscription_period: SubscriptionPeriod):
    user = await get_user(str(query.from_user.id))

    emojis = Subscription.get_emojis()
    price = Subscription.get_price(user.currency, subscription_type, subscription_period)
    name = (f"{subscription_type} {emojis[subscription_type]} "
            f"({get_localization(user.language_code).cycles_subscribe()[subscription_period]})")
    description = get_localization(user.language_code).confirmation_subscribe(subscription_type, subscription_period)

    await query.message.reply_invoice(
        title=name,
        description=description,
        payload=f"{PaymentType.SUBSCRIPTION}:{query.from_user.id}:{subscription_type}:{subscription_period}",
        provider_token=YOOKASSA_TOKEN,
        currency=f"{user.currency}",
        prices=[LabeledPrice(label=name, amount=price * 100)],
    )

    await query.delete_message()


async def handle_package_selection(query: CallbackQuery, package_type: PackageType, context: CallbackContext):
    user = await get_user(str(query.from_user.id))

    if package_type == PackageType.ACCESS_TO_CATALOG:
        price = Package.get_price(user.currency, package_type, 1)
        name = get_localization(user.language_code).ACCESS_TO_CATALOG
        description = get_localization(user.language_code).ACCESS_TO_CATALOG_DESCRIPTION

        await query.message.reply_invoice(
            title=name,
            description=description,
            payload=f"{PaymentType.PACKAGE}:{query.from_user.id}:{package_type}:1",
            provider_token=YOOKASSA_TOKEN,
            currency=f"{user.currency}",
            prices=[LabeledPrice(label=name, amount=price * 100)],
        )

        await query.delete_message()
    elif package_type == PackageType.VOICE_MESSAGES:
        price = Package.get_price(user.currency, package_type, 1)
        name = get_localization(user.language_code).ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES
        description = get_localization(user.language_code).ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES_DESCRIPTION

        await query.message.reply_invoice(
            title=name,
            description=description,
            payload=f"{PaymentType.PACKAGE}:{query.from_user.id}:{package_type}:1",
            provider_token=YOOKASSA_TOKEN,
            currency=f"{user.currency}",
            prices=[LabeledPrice(label=name, amount=price * 100)],
        )

        await query.delete_message()
    elif package_type == PackageType.FAST_MESSAGES:
        price = Package.get_price(user.currency, package_type, 1)
        name = get_localization(user.language_code).FAST_ANSWERS
        description = get_localization(user.language_code).FAST_ANSWERS_DESCRIPTION

        await query.message.reply_invoice(
            title=name,
            description=description,
            payload=f"{PaymentType.PACKAGE}:{query.from_user.id}:{package_type}:1",
            provider_token=YOOKASSA_TOKEN,
            currency=f"{user.currency}",
            prices=[LabeledPrice(label=name, amount=price * 100)],
        )

        await query.delete_message()
    else:
        message = get_localization(user.language_code).choose_min(package_type)

        reply_markup = build_quantity_of_packages_keyboard(user.language_code)

        await query.edit_message_caption(caption=message, parse_mode=PARSE_MODE, reply_markup=reply_markup)
        context.user_data['awaiting_package'] = package_type
        context.user_data['awaiting_quantity'] = True


async def handle_quantity_of_package_selection(query: CallbackQuery, value: str, context: CallbackContext):
    if value == 'exit':
        context.user_data['awaiting_package'] = False
        context.user_data['awaiting_quantity'] = False

        await query.delete_message()


async def handle_catalog_selection(query: CallbackQuery, role_name: str):
    user = await get_user(str(query.from_user.id))

    keyboard = query.message.reply_markup.inline_keyboard
    keyboard_changed = False

    new_keyboard = []
    for row in keyboard:
        new_row = []
        for button in row:
            text = button.text
            callback_data = button.callback_data.split(":", 1)[1]

            if callback_data == role_name:
                if "❌" in text:
                    text = text.replace(" ❌", " ✅")
                    keyboard_changed = True
            else:
                text = text.replace(" ✅", " ❌")
            new_row.append(InlineKeyboardButton(text, callback_data=button.callback_data))
        new_keyboard.append(new_row)

    if keyboard_changed:
        current_chat = await get_chat_by_user_id(user.id)
        await update_chat(current_chat.id, {
            "role": role_name,
            "edited_at": datetime.now(timezone.utc)
        })
        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(new_keyboard))

        message = getattr(get_localization(user.language_code), role_name)["description"]
        await query.message.reply_text(text=message,
                                       parse_mode=PARSE_MODE)


async def handle_chat_selection(query: CallbackQuery, action: str, context: CallbackContext):
    user = await get_user(str(query.from_user.id))

    if action == 'show':
        all_chats = await get_chats_by_user_id(user.id)
        message = ""
        for count, chat in enumerate(all_chats):
            message += f"\n{count + 1}. *{chat.title}*"

        await query.message.reply_text(text=message, parse_mode=PARSE_MODE)
    elif action == 'create':
        if user.additional_usage_quota[UserQuota.ADDITIONAL_CHATS] > 0:
            reply_markup = build_create_chat_keyboard(user.language_code)

            await query.edit_message_text(text=get_localization(user.language_code).TYPE_CHAT_NAME,
                                          reply_markup=reply_markup,
                                          parse_mode=PARSE_MODE)
            context.user_data['awaiting_chat'] = True
        else:
            await query.message.reply_text(text=get_localization(user.language_code).CREATE_CHAT_FORBIDDEN,
                                           parse_mode=PARSE_MODE)
    elif action == 'switch':
        all_chats = await get_chats_by_user_id(user.id)

        if len(all_chats) > 0:
            current_chat = await get_chat_by_user_id(user.id)
            reply_markup = build_switch_chat_keyboard(user.language_code, current_chat.id, all_chats)

            await query.edit_message_text(text=get_localization(user.language_code).SWITCH_CHAT,
                                          reply_markup=reply_markup,
                                          parse_mode=PARSE_MODE)
        else:
            await query.message.reply_text(text=get_localization(user.language_code).SWITCH_CHAT_FORBIDDEN,
                                           parse_mode=PARSE_MODE)
    elif action == 'delete':
        all_chats = await get_chats_by_user_id(user.id)

        if len(all_chats) > 0:
            current_chat = await get_chat_by_user_id(user.id)
            reply_markup = build_delete_chat_keyboard(user.language_code, current_chat.id, all_chats)

            await query.edit_message_text(get_localization(user.language_code).DELETE_CHAT,
                                          reply_markup=reply_markup,
                                          parse_mode=PARSE_MODE)
        else:
            await query.message.reply_text(text=get_localization(user.language_code).DELETE_CHAT_FORBIDDEN,
                                           parse_mode=PARSE_MODE)


async def handle_create_chat_selection(query: CallbackQuery, value: str, context: CallbackContext):
    if value == 'exit':
        context.user_data['awaiting_chat'] = False

        await query.delete_message()


async def handle_switch_chat_selection(query: CallbackQuery, chat_id: str):
    user = await get_user(str(query.from_user.id))

    await update_user(user.id, {
        "current_chat_id": chat_id
    })


async def handle_delete_chat_selection(query: CallbackQuery, chat_id: str):
    user = await get_user(str(query.from_user.id))

    await delete_chat(chat_id)

    await query.message.reply_text(
        text=get_localization(user.language_code).DELETE_CHAT_SUCCESS,
        parse_mode=PARSE_MODE
    )


async def handle_gender_selection(query: CallbackQuery, gender: UserGender, context: CallbackContext):
    user = await get_user(str(query.from_user.id))
    user.gender = gender

    await update_user(user.id, {
        "gender": user.gender,
    })

    text_your_gender = get_localization(user.language_code).YOUR_GENDER
    text_gender_male = get_localization(user.language_code).MALE
    text_gender_female = get_localization(user.language_code).FEMALE
    await query.edit_message_text(
        f"{text_your_gender} {text_gender_male if user.gender == UserGender.MALE else text_gender_female}"
    )

    if user.current_model == Model.FACE_SWAP:
        await handle_face_swap(query.message, context, user)


async def handle_face_swap_choose_selection(query: CallbackQuery, package_name: str, context: CallbackContext):
    user = await get_user(str(query.from_user.id))

    face_swap_package = await get_face_swap_package_by_user_id_and_name(user.id, package_name)
    if face_swap_package is None:
        face_swap_package = await write_face_swap_package(user.id, package_name, {
            UserGender.MALE: [],
            UserGender.FEMALE: []
        })
    face_swap_package_quantity = len(getattr(FaceSwapPackageName, package_name)[f"{user.gender}_files"])
    face_swap_package_name = face_swap_package.name
    if face_swap_package.name == FaceSwapPackageName.CELEBRITIES['name']:
        face_swap_package_name = get_localization(user.language_code).CELEBRITIES
    elif face_swap_package_name == FaceSwapPackageName.MOVIE_CHARACTERS['name']:
        face_swap_package_name = get_localization(user.language_code).MOVIE_CHARACTERS
    elif face_swap_package_name == FaceSwapPackageName.PROFESSIONS['name']:
        face_swap_package_name = get_localization(user.language_code).PROFESSIONS
    elif face_swap_package_name == FaceSwapPackageName.SEVEN_WONDERS_OF_THE_ANCIENT_WORLD['name']:
        face_swap_package_name = get_localization(user.language_code).SEVEN_WONDERS_OF_THE_ANCIENT_WORLD

    reply_markup = build_face_swap_package_keyboard(user.language_code)

    await query.edit_message_text(
        text=get_localization(user.language_code).choose_face_swap_package(
            face_swap_package_name,
            user.monthly_limits[UserQuota.FACE_SWAP] + user.additional_usage_quota[UserQuota.FACE_SWAP],
            face_swap_package_quantity,
            len(face_swap_package.used_images)),
        reply_markup=reply_markup,
        parse_mode=PARSE_MODE)
    context.user_data['awaiting_quantity'] = True
    context.user_data['awaiting_face_swap_package'] = True
    context.user_data['face_swap_package_name'] = face_swap_package.name


async def handle_face_swap_package_selection(query: CallbackQuery, package_name: str, context: CallbackContext):
    if package_name == 'exit':
        context.user_data['awaiting_quantity'] = False

        await query.delete_message()
    elif package_name == 'back':
        user = await get_user(str(query.from_user.id))
        context.user_data['awaiting_quantity'] = False

        reply_markup = build_face_swap_choose_keyboard(user.language_code)
        await query.edit_message_text(text=get_localization(user.language_code).CHOOSE_YOUR_PACKAGE,
                                      reply_markup=reply_markup,
                                      parse_mode=PARSE_MODE)


async def choose_button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    command, value = query.data.split(':', 1)

    if value == 'close':
        await query.message.delete()
    elif command == 'chat_gpt':
        await handle_chat_gpt_selection(query, value, context)
    elif command == 'feedback':
        await handle_feedback_selection(query, value, context)
    elif command == 'language':
        await handle_language_selection(query, value)
    elif command == 'promo_code':
        await handle_promo_code_selection(query, value, context)
    elif command == 'promo_code_admin':
        await handle_promo_code_admin_selection(query, value)
    elif command == 'promo_code_admin_subscription':
        await handle_promo_code_admin_subscription_selection(query, value)
    elif command == 'promo_code_admin_period_of_subscription':
        subscription_period, subscription_type = value.split(':')
        await handle_promo_code_admin_period_of_subscription_selection(query,
                                                                       subscription_type,
                                                                       subscription_period,
                                                                       context)
    elif command == 'promo_code_admin_name':
        await handle_promo_code_admin_name_selection(query, value, context)
    elif command == 'promo_code_admin_date':
        await handle_promo_code_admin_date_selection(query, value, context)
    elif command == 'statistics_admin':
        await handle_statistics_admin_selection(query, value)
    elif command == 'mode':
        await handle_mode_selection(query, value, context)
    elif command == 'profile':
        await handle_profile_selection(query, value, context)
    elif command == 'gender':
        await handle_gender_selection(query, value, context)
    elif command == 'setting':
        await handle_setting_selection(query, value)
    elif command == 'subscription':
        await handle_subscription_selection(query, value)
    elif command == 'period_of_subscription':
        subscription_period, subscription_type = value.split(':')
        await handle_period_of_subscription_selection(query, subscription_type, subscription_period)
    elif command == 'package':
        await handle_package_selection(query, value, context)
    elif command == 'quantity_of_package':
        await handle_quantity_of_package_selection(query, value, context)
    elif command == 'catalog':
        await handle_catalog_selection(query, value)
    elif command == 'chat':
        await handle_chat_selection(query, value, context)
    elif command == 'create_chat':
        await handle_create_chat_selection(query, value, context)
    elif command == 'switch_chat':
        await handle_switch_chat_selection(query, value)
    elif command == 'delete_chat':
        await handle_delete_chat_selection(query, value)
    elif command == 'face_swap_choose':
        await handle_face_swap_choose_selection(query, value, context)
    elif command == 'face_swap_package':
        await handle_face_swap_package_selection(query, value, context)
