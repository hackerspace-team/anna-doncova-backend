import time

from telegram import Update, constants
from telegram.ext import CallbackContext

from app.bot.constants import PARSE_MODE, GPT3_DAILY_LIMIT_MESSAGES
from app.bot.features.chat import get_chat
from app.bot.features.message import write_message, get_messages_by_chat_id
from app.bot.features.user import get_user, update_user
from app.bot.integrations.openAI import get_response_message
from app.bot.locales.main import get_localization
from app.bot.utilities import is_time_limit_exceeded, is_messages_limit_exceeded
from app.models import Model, User


async def handle_chatgpt(update: Update, context: CallbackContext, user: User, current_time: float):
    need_exit = await is_messages_limit_exceeded(update, user)
    if need_exit:
        return

    context.user_data['last_request_time'] = current_time

    await write_message(user.current_chat_id, "user", user.id, update.message.text)

    chat = await get_chat(user.current_chat_id)
    messages = await get_messages_by_chat_id(user.current_chat_id)
    sorted_messages = sorted(messages, key=lambda m: m.created_at)
    history = [{'role': message.sender, 'content': message.content} for message in sorted_messages]

    processing_message = await update.message.reply_text(
        text=get_localization(user.language_code).processing_request(),
        reply_to_message_id=update.message.message_id
    )

    await update.message.chat.send_action(action=constants.ChatAction.TYPING)

    try:
        response_message = get_response_message(user.current_model, history)

        # role, content = ["assistant", "Hello! How can I assist you today?"]
        role, content = response_message.role, response_message.content
        await write_message(user.current_chat_id, role, "", content)

        user.daily_limits["GPT3"] -= 1
        await update_user(user.id, {"daily_limits": user.daily_limits})
        await update.message.reply_text(
            f"💬 {chat.title}\n\n{content}\n\n✉️ {user.daily_limits['GPT3'] + 1}/{GPT3_DAILY_LIMIT_MESSAGES}",
            parse_mode=PARSE_MODE,
            reply_to_message_id=update.message.message_id,
        )
    except Exception as e:
        await update.message.reply_text(
            f"I've got an error: {e}\n\nPlease contact @roman_danilov",
            parse_mode=PARSE_MODE
        )
    finally:
        await processing_message.delete()


async def handle_message(update: Update, context: CallbackContext):
    if update.edited_message or not update.message or update.message.via_bot or update.message.text.startswith('/'):
        return

    user = await get_user(str(update.effective_user.id))
    current_time = time.time()

    need_exit = await is_time_limit_exceeded(update, context, user, current_time)
    if need_exit:
        return

    if user.current_model == Model.GPT3.value:
        await handle_chatgpt(update, context, user, current_time)
