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


async def reset_daily_limits(context: CallbackContext):
    all_users = await get_users()
    for i in range(0, len(all_users), USER_BATCH_SIZE):
        batch = db.batch()
        user_batch = all_users[i:i + USER_BATCH_SIZE]

        for user in user_batch:
            user_ref = db.collection("users").document(user.id)
            batch.update(user_ref, {
                "daily_limits": User.DEFAULT_DAILY_LIMITS,
            })

            await context.bot.send_message(
                chat_id=user.telegram_chat_id,
                text="Your daily limits have been reset!"
            )

        await batch.commit()
