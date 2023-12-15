from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, LabeledPrice
from telegram.ext import CallbackContext

from AnnaDoncovaBackend.settings import YOOKASSA_TOKEN
from app.bot.constants import PARSE_MODE
from app.bot.features.chat import get_chat_by_user_id, update_chat, get_chats_by_user_id, delete_chat
from app.bot.features.face_swap_package import get_face_swap_package_by_user_id_and_name, write_face_swap_package
from app.bot.features.user import update_user, get_user
from app.bot.helpers import handle_face_swap
from app.bot.keyboards import (build_period_of_subscription_keyboard,
                               build_quantity_of_packages_keyboard,
                               build_create_chat_keyboard,
                               build_switch_chat_keyboard,
                               build_delete_chat_keyboard, build_face_swap_package_keyboard,
                               build_face_swap_choose_keyboard)
from app.bot.locales.main import get_localization
from app.models import (SubscriptionType,
                        SubscriptionPeriod,
                        Subscription,
                        PackageType,
                        Package,
                        Role,
                        UserQuota,
                        Model,
                        UserGender,
                        FaceSwapPackageName)


async def handle_language_selection(query: CallbackQuery, chosen_language: str):
    await update_user(str(query.from_user.id), {"language_code": chosen_language})

    await query.edit_message_text(text=get_localization(chosen_language).CHOOSE_LANGUAGE, parse_mode=PARSE_MODE)


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

    if mode == Model.Face_Swap:
        user = await get_user(str(query.from_user.id))

        await handle_face_swap(query.message, context, user)


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
        payload=f"SUBSCRIPTION:{query.from_user.id}:{subscription_type}:{subscription_period}",
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
            payload=f"PACKAGE:{query.from_user.id}:{package_type}:1",
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
            payload=f"PACKAGE:{query.from_user.id}:{package_type}:1",
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
            payload=f"PACKAGE:{query.from_user.id}:{package_type}:1",
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
        role_description = getattr(Role, role_name)["description"]
        await update_chat(current_chat.id, {
            "role": {
                "name": role_name,
                "description": role_description,
            },
            "edited_at": datetime.now()
        })
        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(new_keyboard))


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


async def handle_face_swap_gender_selection(query: CallbackQuery, gender: UserGender, context: CallbackContext):
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

    await handle_face_swap(query.message, context, user)


async def handle_face_swap_choose_selection(query: CallbackQuery, package_name: str, context: CallbackContext):
    user = await get_user(str(query.from_user.id))

    face_swap_package = await get_face_swap_package_by_user_id_and_name(user.id, package_name)
    if face_swap_package is None:
        face_swap_package = await write_face_swap_package(user.id, package_name, [])
    face_swap_package_quantity = len(getattr(FaceSwapPackageName, package_name)[f"{user.gender}_files"])
    face_swap_package_name = face_swap_package.name
    if face_swap_package.name == FaceSwapPackageName.CELEBRITIES['name']:
        face_swap_package_name = get_localization(user.language_code).CELEBRITIES

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
    elif command == 'language':
        await handle_language_selection(query, value)
    elif command == 'mode':
        await handle_mode_selection(query, value, context)
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
    elif command == 'face_swap_gender':
        await handle_face_swap_gender_selection(query, value, context)
    elif command == 'face_swap_choose':
        await handle_face_swap_choose_selection(query, value, context)
    elif command == 'face_swap_package':
        await handle_face_swap_package_selection(query, value, context)
