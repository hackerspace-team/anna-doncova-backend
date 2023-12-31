import asyncio

from rest_framework import generics, status
from rest_framework.response import Response

from .features.application import write_application
from .helpers import send_message_to_admins
from .models.application import ApplicationType
from .seriallizers import PreRegisterSerializer


class PreRegisterView(generics.CreateAPIView):
    serializer_class = PreRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        name, phone, email, activities = data['name'], data['phone'], data['email'], data['activities']

        message = (f"#application\n\n"
                   f"🚀 <b>Новый клиент на курсах по нейросетям!</b>\n\n"
                   f"👤 Имя: {name}\n"
                   f"📞 Телефон: {phone}\n"
                   f"📧 Почта: {email}\n"
                   f"🧠 Деятельность: {'Не указана' if len(activities) == 0 else ', '.join(activities)}\n\n"
                   f"📄 Форма: Предзапись")
        asyncio.run(send_message_to_admins(message))
        asyncio.run(write_application(name, phone, email, activities, ApplicationType.PRE_REGISTER))

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
