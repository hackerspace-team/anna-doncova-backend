from datetime import datetime, timezone

from telegram.ext import CallbackContext

from app.bot.constants import USER_BATCH_SIZE
from app.bot.features.package import get_packages_by_user_id
from app.bot.features.subscription import get_last_subscription_by_user_id, update_subscription
from app.bot.features.user import get_users
from app.bot.locales.main import get_localization
from app.firebase import db
from app.models.package import PackageType
from app.models.subscription import SubscriptionType, SubscriptionStatus
from app.models.user import User, UserQuota, UserSettings


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

            current_date = datetime.now(timezone.utc)
            is_time_to_update_limits = (current_date - user.last_subscription_limit_update).days >= 30
            if user.last_subscription_limit_update and is_time_to_update_limits:
                current_subscription = await get_last_subscription_by_user_id(user.id)
                if current_subscription.end_date <= current_date:
                    packages = await get_packages_by_user_id(user.id)
                    user.additional_usage_quota[UserQuota.VOICE_MESSAGES] = False
                    user.additional_usage_quota[UserQuota.FAST_MESSAGES] = False
                    user.additional_usage_quota[UserQuota.ACCESS_TO_CATALOG] = False
                    for package in packages:
                        if package.type == PackageType.VOICE_MESSAGES:
                            user.additional_usage_quota[UserQuota.VOICE_MESSAGES] = True
                        elif package.type == PackageType.FAST_MESSAGES:
                            user.additional_usage_quota[UserQuota.FAST_MESSAGES] = True
                        elif package.type == PackageType.ACCESS_TO_CATALOG:
                            user.additional_usage_quota[UserQuota.ACCESS_TO_CATALOG] = True

                    if not user.additional_usage_quota[UserQuota.VOICE_MESSAGES]:
                        user.settings[UserSettings.TURN_ON_VOICE_MESSAGES] = False

                    await update_subscription(current_subscription.id, {
                        "status": SubscriptionStatus.FINISHED,
                    })
                    batch.update(user_ref, {
                        "monthly_limits": User.DEFAULT_MONTHLY_LIMITS[SubscriptionType.FREE],
                        "additional_usage_quota": user.additional_usage_quota,
                        "settings": user.settings,
                        "last_subscription_limit_update": datetime.now()
                    })

                    for telegram_chat_id in user.telegram_chat_ids:
                        await context.bot.send_message(
                            chat_id=telegram_chat_id,
                            text=get_localization(user.language_code).SUBSCRIPTION_END
                        )
                else:
                    batch.update(user_ref, {
                        "monthly_limits": User.DEFAULT_MONTHLY_LIMITS[user.subscription_type],
                        "last_subscription_limit_update": datetime.now()
                    })

                    for telegram_chat_id in user.telegram_chat_ids:
                        await context.bot.send_message(
                            chat_id=telegram_chat_id,
                            text=get_localization(user.language_code).SUBSCRIPTION_RESET
                        )

        await batch.commit()
