from telegram import Update
from telegram.ext import CallbackContext

from app.bot.constants import PARSE_MODE
from app.bot.features.package import write_package, get_last_package_by_user_id
from app.bot.features.subscription import write_subscription, get_last_subscription_by_user_id
from app.bot.features.user import get_user
from app.bot.helpers import create_subscription, create_package
from app.bot.locales.main import get_localization
from app.firebase import db
from app.models import SubscriptionStatus, PackageStatus


async def pre_checkout(update: Update, context: CallbackContext):
    query = update.pre_checkout_query

    payment_type = query.invoice_payload.split(':')[0]
    if payment_type == 'SUBSCRIPTION':
        _, user_id, subscription_type, subscription_period = query.invoice_payload.split(':')
        try:
            await write_subscription(user_id,
                                     subscription_type,
                                     subscription_period,
                                     SubscriptionStatus.WAITING,
                                     query.currency,
                                     query.total_amount // 100)
            await query.answer(ok=True)
        except Exception:
            await query.answer(ok=False)
    elif payment_type == 'PACKAGE':
        _, user_id, package_type, quantity = query.invoice_payload.split(':')
        try:
            await write_package(user_id,
                                package_type,
                                PackageStatus.WAITING,
                                query.currency,
                                query.total_amount // 100,
                                int(quantity))
            await query.answer(ok=True)
        except Exception:
            await query.answer(ok=False)
    else:
        await query.answer(ok=False)


async def successful(update: Update, context: CallbackContext):
    payment = update.message.successful_payment
    payment_type = payment.invoice_payload.split(':')[0]
    if payment_type == 'SUBSCRIPTION':
        user_id = str(update.effective_user.id)
        user = await get_user(user_id)
        subscription = await get_last_subscription_by_user_id(user_id)

        transaction = db.transaction()
        await create_subscription(transaction,
                                  subscription.id,
                                  subscription.user_id,
                                  update.message.successful_payment.provider_payment_charge_id)

        await update.message.reply_text(text=get_localization(user.language_code).SUBSCRIPTION_SUCCESS,
                                        parse_mode=PARSE_MODE)
    elif payment_type == 'PACKAGE':
        user_id = str(update.effective_user.id)
        user = await get_user(user_id)
        package = await get_last_package_by_user_id(user_id)

        transaction = db.transaction()
        await create_package(transaction,
                             package.id,
                             package.user_id,
                             update.message.successful_payment.provider_payment_charge_id)

        await update.message.reply_text(text=get_localization(user.language_code).PACKAGE_SUCCESS,
                                        parse_mode=PARSE_MODE)
