from datetime import datetime, timezone

from telegram.ext import CallbackContext

from app.bot.constants import USER_BATCH_SIZE
from app.bot.features.user import get_users
from app.bot.locales.main import get_localization
from app.firebase import db
from app.models import User


async def update_waiting_message(context: CallbackContext):
    data = context.job.data

    await context.bot.send_message(
        context.job.chat_id,
        get_localization(data["language_code"]).READY_FOR_NEW_REQUEST,
        reply_to_message_id=data["message_id"]
    )


async def reset_monthly_limits(context: CallbackContext):
    all_users = await get_users()
    for i in range(0, len(all_users), USER_BATCH_SIZE):
        batch = db.batch()
        user_batch = all_users[i:i + USER_BATCH_SIZE]

        for user in user_batch:
            user_ref = db.collection("users").document(user.id)
            user_data = (await user_ref.get()).to_dict() or {}

            last_update_date = user_data.get('last_subscription_limit_update')
            is_time_to_update_limits = (datetime.now(timezone.utc) - last_update_date).days >= 30
            if last_update_date and is_time_to_update_limits:
                batch.update(user_ref, {
                    "monthly_limits": User.DEFAULT_MONTHLY_LIMITS[user.subscription_type],
                })

                for telegram_chat_id in user.telegram_chat_ids:
                    await context.bot.send_message(
                        chat_id=telegram_chat_id,
                        text="Your monthly limits have been reset!"
                    )

        await batch.commit()
