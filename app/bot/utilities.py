from telegram import Update
from telegram.ext import CallbackContext

from app.bot.constants import LIMIT_BETWEEN_REQUESTS_SECONDS
from app.bot.handlers.job_handlers import update_waiting_message
from app.bot.locales.main import get_localization
from app.models import User


async def is_time_limit_exceeded(update: Update, context: CallbackContext, user: User, current_time: float) -> bool:
    if 'last_request_time' in context.user_data:
        time_elapsed = current_time - context.user_data['last_request_time']
        if time_elapsed < LIMIT_BETWEEN_REQUESTS_SECONDS:
            remaining_time = int(LIMIT_BETWEEN_REQUESTS_SECONDS - time_elapsed)

            if 'additional_request_made' in context.user_data:
                await update.message.reply_text(
                    text=get_localization(user.language_code).ALREADY_MAKE_REQUEST,
                    reply_to_message_id=update.message.message_id
                )
                return True

            context.user_data['additional_request_made'] = True
            await update.message.reply_text(
                text=get_localization(user.language_code).wait_for_another_request(remaining_time),
                reply_to_message_id=update.message.message_id
            )
            context.job_queue.run_once(
                update_waiting_message,
                remaining_time,
                user_id=update.effective_user.id,
                chat_id=update.effective_message.chat_id,
                data={"message_id": update.message.message_id, "language_code": user.language_code}
            )
            return True
        else:
            del context.user_data['last_request_time']
            if 'additional_request_made' in context.user_data:
                del context.user_data['additional_request_made']

        return False


async def is_messages_limit_exceeded(update: Update, user: User):
    if user.daily_limits["GPT3"] < 1:
        await update.message.reply_text(
            "You've reached a daily limit",
            reply_to_message_id=update.message.message_id
        )
        return True

    return False
