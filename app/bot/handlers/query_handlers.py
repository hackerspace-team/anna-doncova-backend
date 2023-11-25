from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import CallbackContext

from app.bot.constants import PARSE_MODE
from app.bot.features.user import update_user
from app.bot.locales.main import get_localization


async def handle_language_selection(query: CallbackQuery, chosen_language: str, update: Update):
    await update_user(str(update.effective_user.id), {"language_code": chosen_language})

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
        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(new_keyboard))


async def choose_button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    command, value = query.data.split(':', 1)

    if value == 'close':
        await query.message.delete()
    elif command == 'language':
        await handle_language_selection(query, value, update)
    elif command == 'mode':
        await handle_mode_selection(query, value)
