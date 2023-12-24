import asyncio
from enum import Enum
from rest_framework import generics, status
from rest_framework.response import Response
from telegram import Bot

from AnnaDoncovaBackend.settings import TELEGRAM_TOKEN, ADMIN_CHAT_IDS
from app.bot.features.application import write_application
from .seriallizers import PreRegisterSerializer


async def send_message_to_admins(message):
    bot = Bot(token=TELEGRAM_TOKEN)

    for chat_id in ADMIN_CHAT_IDS:
        await bot.send_message(chat_id=chat_id, text=message)


class Application(Enum):
    PRE_REGISTER = 'PRE_REGISTER'
    REGISTER = 'REGISTER'


class PreRegisterView(generics.CreateAPIView):
    serializer_class = PreRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        name, phone, email, activities = data['name'], data['phone'], data['email'], data['activities']

        message = (f"#application\n\n"
                   f"🚀 Новый клиент на курсах по нейросетям! 🚀\n\n"
                   f"👤 Имя: {name}\n"
                   f"📞 Телефон: {phone}\n"
                   f"📧 Почта: {email}\n"
                   f"🧠 Деятельность: {'Не указана' if len(activities) == 0 else ', '.join(activities)}\n\n"
                   f"📄 Форма: Предзапись")
        asyncio.run(send_message_to_admins(message))

        write_application(name, phone, email, activities, Application.PRE_REGISTER.value)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
