from telegram import Update
from telegram.ext import CallbackContext

from app.bot.constants import LIMIT_BETWEEN_REQUESTS_SECONDS
from app.bot.handlers.job_handlers import update_waiting_message
from app.bot.locales.main import get_localization
from app.models.common import Model
from app.models.user import User, UserQuota


async def is_time_limit_exceeded(update: Update, context: CallbackContext, user: User, current_time: float) -> bool:
    if user.additional_usage_quota[UserQuota.FAST_MESSAGES]:
        return False

    if 'last_request_time' in context.user_data and user.current_model != Model.Face_Swap:
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


async def is_messages_limit_exceeded(update: Update, user: User, user_quota: UserQuota):
    if user.monthly_limits[user_quota] < 1 and user.additional_usage_quota[user_quota]:
        await update.message.reply_text(
            f"You've reached a monthly limit in {user_quota}",
            reply_to_message_id=update.message.message_id
        )
        return True

    return False


def is_awaiting_something(context: CallbackContext):
    return (context.user_data.get('awaiting_quantity', False) or
            context.user_data.get('awaiting_package', False) or
            context.user_data.get('awaiting_chat', False) or
            context.user_data.get('awaiting_feedback', False) or
            context.user_data.get('awaiting_promo_code', False) or
            context.user_data.get('awaiting_promo_code_name', False) or
            context.user_data.get('awaiting_promo_code_date', False))
