from telegram import Update, constants
from telegram.ext import CallbackContext

from AnnaDoncovaBot.settings import ADMIN_CHAT_IDS
from AnnaDoncovaBot.constants import PARSE_MODE
from AnnaDoncovaBot.features.application import get_applications


async def applications(update: Update, context: CallbackContext):
    is_admin = update.message.chat_id in ADMIN_CHAT_IDS
    if is_admin:
        await update.get_bot().send_chat_action(chat_id=update.message.chat_id, action=constants.ChatAction.TYPING)

        list_of_applications = await get_applications()
        for application in list_of_applications:
            message = (f"#application\n\n"
                       f"🚀 <b>Клиент на курсах по нейросетям!</b>\n\n"
                       f"👤 Имя: {application.name}\n"
                       f"📞 Телефон: {application.phone}\n"
                       f"📧 Почта: {application.email}\n"
                       f"🧠 Деятельность: {'Не указана' if len(application.activities) == 0 else ', '.join(application.activities)}\n\n"
                       f"📄 Форма: Предзапись\n"
                       f"🗓 Дата заполнения: {application.created_date.strftime('%d.%m.%Y %H:%M')}")
            await update.message.reply_text(text=message,
                                            parse_mode=PARSE_MODE)
