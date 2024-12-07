import pytz
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from telegram import constants

from AnnaDoncovaBot.config import config
from AnnaDoncovaBot.features.application import get_applications
from AnnaDoncovaBot.features.enrollment import get_enrollments
from AnnaDoncovaBot.features.mini_course import get_mini_courses
from AnnaDoncovaBot.models.enrollment import PaymentType, PaymentMethod

common_router = Router()


@common_router.message(Command("applications"))
async def applications(message: Message):
    is_admin = str(message.chat.id) in config.ADMIN_CHAT_IDS
    if is_admin:
        await message.bot.send_chat_action(chat_id=message.chat.id, action=constants.ChatAction.TYPING)

        list_of_applications = await get_applications()
        for application in list_of_applications:
            created_at_pst = (application.created_date
                              .astimezone(pytz.timezone('America/Los_Angeles'))
                              .strftime('%d.%m.%Y %H:%M'))
            text = (f"#application\n\n"
                    f"🚀 <b>Запись на мастер-класс по нейросетям!</b>\n\n"
                    f"ℹ️ ID: {application.id}\n"
                    f"👤 Имя: {application.name}\n"
                    f"📞 Телефон: {application.phone}\n"
                    f"📧 Почта: {application.email}\n"
                    f"✈️ Телеграм: {application.telegram if application.telegram else 'Не указан'}\n"
                    f"🧠 Деятельность: {'Не указана' if len(application.activities) == 0 else ', '.join(application.activities)}\n\n"
                    f"📄 Форма: Предзапись\n"
                    f"🗓 Дата заполнения по PST: {created_at_pst}")
            await message.answer(text=text)


@common_router.message(Command("enrollments"))
async def enrollments(message: Message):
    is_admin = str(message.chat.id) in config.ADMIN_CHAT_IDS
    if is_admin:
        await message.bot.send_chat_action(chat_id=message.chat.id, action=constants.ChatAction.TYPING)

        list_of_enrollments = await get_enrollments()
        for enrollment in list_of_enrollments:
            created_at_pst = (enrollment.created_date
                              .astimezone(pytz.timezone('America/Los_Angeles'))
                              .strftime('%d.%m.%Y %H:%M'))
            text = (f"#enrollment\n\n"
                    f"🚀 <b>Клиент на курсах по нейросетям!</b>\n\n"
                    f"ℹ️ ID: {enrollment.id}\n"
                    f"👤 Имя: {enrollment.name}\n"
                    f"📞 Телефон: {enrollment.phone}\n"
                    f"📧 Почта: {enrollment.email}\n"
                    f"✈️ Телеграм: {enrollment.telegram if enrollment.telegram else 'Не указан'}\n"
                    f"🧠 Деятельность: {enrollment.activity if enrollment.activity else 'Не указана'}\n"
                    f"⭐ Тариф: {enrollment.tariff}\n"
                    f"🏦 Предоплата: {'Да' if enrollment.payment_type == PaymentType.PREPAYMENT else 'Нет'}\n"
                    f"💱 Метод оплаты: {'PayPal' if enrollment.payment_method == PaymentMethod.PAYPAL else 'ЮKassa'}\n"
                    f"💸 Сумма: {enrollment.amount}{'$' if enrollment.payment_method == PaymentMethod.PAYPAL else '₽'}\n"
                    f"🤑 Чистая сумма: {enrollment.income_amount}₽\n"
                    f"👁 Статус: {enrollment.payment_status}\n\n"
                    f"📄 Форма: Запись\n"
                    f"🗓 Дата заполнения по PST: {created_at_pst}")
            await message.answer(text=text)


@common_router.message(Command("mini_courses"))
async def mini_courses(message: Message):
    is_admin = str(message.chat.id) in config.ADMIN_CHAT_IDS
    if is_admin:
        await message.bot.send_chat_action(chat_id=message.chat.id, action=constants.ChatAction.TYPING)

        list_of_mini_courses = await get_mini_courses()
        for mini_course in list_of_mini_courses:
            created_at_pst = (mini_course.created_date
                              .astimezone(pytz.timezone('America/Los_Angeles'))
                              .strftime('%d.%m.%Y %H:%M'))
            text = (f"#mini_course\n\n"
                    f"🚀 <b>Клиент на мини-курсе!</b>\n\n"
                    f"ℹ️ ID: {mini_course.id}\n"
                    f"👤 Имя: {mini_course.name}\n"
                    f"📧 Почта: {mini_course.email}\n"
                    f"✈️ Телеграм: {mini_course.telegram if mini_course.telegram else 'Не указан'}\n"
                    f"💱 Метод оплаты: {'PayPal' if mini_course.payment_method == PaymentMethod.PAYPAL else 'ЮKassa'}\n"
                    f"💸 Сумма: {mini_course.amount}{'$' if mini_course.payment_method == PaymentMethod.PAYPAL else '₽'}\n"
                    f"🤑 Чистая сумма: {mini_course.income_amount}₽\n"
                    f"👁 Статус: {mini_course.payment_status}\n\n"
                    f"📄 Форма: Запись\n"
                    f"🗓 Дата заполнения по PST: {created_at_pst}")
            await message.answer(text=text)
