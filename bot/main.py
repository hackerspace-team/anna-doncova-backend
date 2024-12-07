import logging
import os
from contextlib import asynccontextmanager

import pytz
import uvicorn
from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from yookassa.domain.notification import WebhookNotification

from AnnaDoncovaBot.config import config
from AnnaDoncovaBot.features.enrollment import get_enrollment_by_payment_id, update_enrollment
from AnnaDoncovaBot.features.mini_course import get_mini_course_by_payment_id, update_mini_course
from AnnaDoncovaBot.handlers.common_handler import common_router
from AnnaDoncovaBot.helpers.send_chat_action_to_admins import send_chat_action_to_admins
from AnnaDoncovaBot.helpers.send_email import send_email
from AnnaDoncovaBot.helpers.send_message_to_admins import send_message_to_admins
from AnnaDoncovaBot.models.enrollment import PaymentType, PaymentStatus

BOT_WEBHOOK_PATH = f"/bot/{config.BOT_TOKEN.get_secret_value()}"
BOT_WEBHOOK_URL = config.SERVER_URL + BOT_WEBHOOK_PATH

YOOKASSA_WEBHOOK_PATH = "/payment/yookassa"
YOOKASSA_WEBHOOK_URL = config.SERVER_URL + YOOKASSA_WEBHOOK_PATH

bot = Bot(token=config.BOT_TOKEN.get_secret_value(), parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage(), sm_strategy=FSMStrategy.GLOBAL_USER)


@asynccontextmanager
async def lifespan(_: FastAPI):
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != BOT_WEBHOOK_URL:
        await bot.set_webhook(url=BOT_WEBHOOK_URL)

    dp.include_router(common_router)
    yield
    await bot.session.close()


app = FastAPI(lifespan=lifespan)


@app.post(BOT_WEBHOOK_PATH)
async def bot_webhook(update: dict):
    try:
        telegram_update = types.Update(**update)
        await dp.feed_update(bot=bot, update=telegram_update)
    except Exception as e:
        logging.exception(f"Error in bot_webhook: {e}")


@app.post(YOOKASSA_WEBHOOK_PATH)
async def yookassa_webhook(request: dict):
    notification_object = WebhookNotification(request)
    payment = notification_object.object

    await send_chat_action_to_admins(bot)

    try:
        enrollment = await get_enrollment_by_payment_id(payment.id)
        if enrollment:
            created_at_pst = (enrollment.created_date
                              .astimezone(pytz.timezone('America/Los_Angeles'))
                              .strftime('%d.%m.%Y %H:%M'))
            if payment.status == 'succeeded':
                text = (f"#payment #succeeded\n\n"
                        f"💰 <b>Оплата курса по нейросетям!</b>\n\n"
                        f"ℹ️ ID: {enrollment.id}\n"
                        f"👤 Имя: {enrollment.name}\n"
                        f"📞 Телефон: {enrollment.phone}\n"
                        f"📧 Почта: {enrollment.email}\n"
                        f"✈️ Телеграм: {enrollment.telegram if enrollment.telegram else 'Не указан'}\n"
                        f"🧠 Деятельность: {enrollment.activity if enrollment.activity else 'Не указана'}\n"
                        f"⭐ Тариф: {enrollment.tariff}\n"
                        f"🏦 Предоплата: {'Да' if enrollment.payment_type == PaymentType.PREPAYMENT else 'Нет'}\n"
                        f"💱 Метод оплаты: ЮKassa\n"
                        f"💸 Сумма: {enrollment.amount}₽\n"
                        f"🤑 Чистая сумма: {payment.income_amount.value}₽\n"
                        f"👁 Статус: Оплачен\n"
                        f"🗓 Дата заполнения по PST: {created_at_pst}")
                await send_message_to_admins(bot, text)

                await update_enrollment(enrollment.id, {
                    "payment_status": PaymentStatus.SUCCEEDED,
                    "income_amount": float(payment.income_amount.value),
                })
            elif payment.status == 'canceled':
                text = (f"#payment #canceled\n\n"
                        f"❌ <b>Отмена оплаты курса по нейросетям!</b>\n\n"
                        f"ℹ️ ID: {enrollment.id}\n"
                        f"👤 Имя: {enrollment.name}\n"
                        f"📞 Телефон: {enrollment.phone}\n"
                        f"📧 Почта: {enrollment.email}\n"
                        f"✈️ Телеграм: {enrollment.telegram if enrollment.telegram else 'Не указан'}\n"
                        f"🧠 Деятельность: {enrollment.activity if enrollment.activity else 'Не указана'}\n"
                        f"⭐ Тариф: {enrollment.tariff}\n"
                        f"🏦 Предоплата: {'Да' if enrollment.payment_type == PaymentType.PREPAYMENT else 'Нет'}\n"
                        f"💱 Метод оплаты: ЮKassa\n"
                        f"💸 Сумма: {enrollment.amount}₽\n"
                        f"👁 Статус: Отменён\n"
                        f"🗓 Дата заполнения по PST: {created_at_pst}")
                await send_message_to_admins(bot, text)

                await update_enrollment(enrollment.id, {
                    "payment_status": PaymentStatus.CANCELED,
                    "income_amount": float(0),
                })
            else:
                text = (f"#error\n\n"
                        f"🚫 <b>Неизвестный статус!</b>\n\n"
                        f"ℹ️ ID: {enrollment.id}\n"
                        f"📄 Статус: {payment.status}\n")
                await send_message_to_admins(bot, text)
    except Exception as e:
        logging.exception(f"Error in yookassa_webhook: {e}")

    try:
        mini_course = await get_mini_course_by_payment_id(payment.id)
        if mini_course:
            created_at_pst = (mini_course.created_date
                              .astimezone(pytz.timezone('America/Los_Angeles'))
                              .strftime('%d.%m.%Y %H:%M'))
            if payment.status == 'succeeded':
                text = (f"#payment #succeeded\n\n"
                        f"💰 <b>Оплата мини-курса!</b>\n\n"
                        f"ℹ️ ID: {mini_course.id}\n"
                        f"👤 Имя: {mini_course.name}\n"
                        f"📧 Почта: {mini_course.email}\n"
                        f"✈️ Телеграм: {mini_course.telegram if mini_course.telegram else 'Не указан'}\n"
                        f"💱 Метод оплаты: ЮKassa\n"
                        f"💸 Сумма: {mini_course.amount}₽\n"
                        f"🤑 Чистая сумма: {payment.income_amount.value}₽\n"
                        f"👁 Статус: Оплачен\n"
                        f"🗓 Дата заполнения по PST: {created_at_pst}")

                await send_email(mini_course.name, mini_course.email)

                await send_message_to_admins(bot, text)

                await update_mini_course(mini_course.id, {
                    "payment_status": PaymentStatus.SUCCEEDED,
                    "income_amount": float(payment.income_amount.value),
                })
            elif payment.status == 'canceled':
                text = (f"#payment #canceled\n\n"
                        f"❌ <b>Отмена оплаты мини-курса!</b>\n\n"
                        f"ℹ️ ID: {mini_course.id}\n"
                        f"👤 Имя: {mini_course.name}\n"
                        f"📧 Почта: {mini_course.email}\n"
                        f"✈️ Телеграм: {mini_course.telegram if mini_course.telegram else 'Не указан'}\n"
                        f"💱 Метод оплаты: ЮKassa\n"
                        f"💸 Сумма: {mini_course.amount}₽\n"
                        f"👁 Статус: Отменён\n"
                        f"🗓 Дата заполнения по PST: {created_at_pst}")
                await send_message_to_admins(bot, text)

                await update_mini_course(mini_course.id, {
                    "payment_status": PaymentStatus.CANCELED,
                    "income_amount": float(0),
                })
            else:
                text = (f"#error\n\n"
                        f"🚫 <b>Неизвестный статус оплаты для мини-курса!</b>\n\n"
                        f"ℹ️ ID: {mini_course.id}\n"
                        f"📄 Статус: {payment.status}\n")
                await send_message_to_admins(bot, text)
    except Exception as e:
        logging.exception(f"Error in yookassa_webhook: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=os.getenv('PORT', 8080))
