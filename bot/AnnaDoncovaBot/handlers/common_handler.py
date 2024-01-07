from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from telegram import constants

from AnnaDoncovaBot.config import config
from AnnaDoncovaBot.features.application import get_applications

common_router = Router()


@common_router.message(Command("applications"))
async def applications(message: Message):
    is_admin = str(message.chat.id) in config.ADMIN_CHAT_IDS
    if is_admin:
        await message.bot.send_chat_action(chat_id=message.chat.id, action=constants.ChatAction.TYPING)

        list_of_applications = await get_applications()
        for application in list_of_applications:
            text = (f"#application\n\n"
                    f"🚀 <b>Клиент на курсах по нейросетям!</b>\n\n"
                    f"👤 Имя: {application.name}\n"
                    f"📞 Телефон: {application.phone}\n"
                    f"📧 Почта: {application.email}\n"
                    f"🧠 Деятельность: {'Не указана' if len(application.activities) == 0 else ', '.join(application.activities)}\n\n"
                    f"📄 Форма: Предзапись\n"
                    f"🗓 Дата заполнения: {application.created_date.strftime('%d.%m.%Y %H:%M')}")
            await message.answer(text=text)
