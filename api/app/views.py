import logging
import traceback

from adrf.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .features.application import write_application
from .helpers import send_message_to_admins
from .models.application import ApplicationType
from .seriallizers import PreRegisterSerializer


class PreRegisterView(APIView):
    async def post(self, request, *args, **kwargs):
        serializer = PreRegisterSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)

            data = serializer.validated_data
            (name,
             phone,
             email,
             telegram,
             activities) = (data['name'],
                            data['phone'],
                            data['email'],
                            data.get('telegram'),
                            data['activities'])

            message = (f"#application\n\n"
                       f"🚀 <b>Новый клиент на курсах по нейросетям!</b>\n\n"
                       f"👤 Имя: {name}\n"
                       f"📞 Телефон: {phone}\n"
                       f"📧 Почта: {email}\n"
                       f"✈️ Телеграм: {telegram if telegram else 'Не указан'}\n"
                       f"🧠 Деятельность: {'Не указана' if len(activities) == 0 else ', '.join(activities)}\n\n"
                       f"📄 Форма: Предзапись")
            await send_message_to_admins(message)
            await write_application(name, phone, email, telegram, activities, ApplicationType.PRE_REGISTER)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as error:
            error_trace = traceback.format_exc()
            logging.error(error, error_trace)
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
