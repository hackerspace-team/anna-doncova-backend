from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, LabeledPrice
from telegram.ext import CallbackContext

from AnnaDoncovaBackend.settings import YOOKASSA_TOKEN
from app.bot.constants import PARSE_MODE
from app.bot.features.user import update_user, get_user
from app.bot.keyboards import build_period_of_subscription_keyboard
from app.bot.locales.main import get_localization
from app.models import SubscriptionType, SubscriptionPeriod, Subscription


async def handle_language_selection(query: CallbackQuery, chosen_language: str):
    await update_user(str(query.from_user.id), {"language_code": chosen_language})

    await query.edit_message_text(text=get_localization(chosen_language).CHOOSE_LANGUAGE, parse_mode=PARSE_MODE)


async def handle_mode_selection(query: CallbackQuery, mode: str):
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


async def handle_setting_selection(query: CallbackQuery, setting: str):
    user = await get_user(str(query.from_user.id))
    user.settings[setting] = not user.settings[setting]

    await update_user(str(query.from_user.id), {"settings": user.settings})


async def handle_subscription_selection(query: CallbackQuery, subscription_type: SubscriptionType, language_code: str):
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


async def choose_button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    command, value = query.data.split(':', 1)

    if value == 'close':
        await query.message.delete()
    elif command == 'language':
        await handle_language_selection(query, value)
    elif command == 'mode':
        await handle_mode_selection(query, value)
    elif command == 'setting':
        await handle_setting_selection(query, value)
    elif command == 'subscription':
        language_code = (await get_user(str(query.from_user.id))).language_code
        await handle_subscription_selection(query, value, language_code)
    elif command == 'period_of_subscription':
        subscription_period, subscription_type = value.split(':')
        await handle_period_of_subscription_selection(query, subscription_type, subscription_period)
