import asyncio
from datetime import datetime
from enum import Enum

from rest_framework import generics, status
from rest_framework.response import Response

from .firebase import db
from .seriallizers import PreRegisterSerializer
from .telegram import send_message_to_admins


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

        print(activities)

        message = (f"🚀 Новый клиент на курсах по нейросетям! 🚀\n\n"
                   f"👤 Имя: {name}\n"
                   f"📞 Телефон: {phone}\n"
                   f"📧 Почта: {email}\n"
                   f"🧠 Деятельность: {'Не указана' if len(activities) == 0 else ', '.join(activities)}\n\n"
                   f"📄 Форма: Предзапись")
        asyncio.run(send_message_to_admins(message))

        db.collection('applications').document().set({
            'name': name,
            'phone': phone,
            'email': email,
            'activities': activities,
            'type': Application.PRE_REGISTER.name,
            'createdDate': datetime.now(),
        })

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
