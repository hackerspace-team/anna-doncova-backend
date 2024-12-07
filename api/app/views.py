import logging
import traceback

from adrf.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .features.application import write_application
from .features.enrollment import write_enrollment
from .features.mini_course import write_mini_course
from .firebase import db
from .helpers import send_message_to_admins, create_payment
from .models.enrollment import PaymentType, PaymentMethod, PaymentStatus, TariffType
from .seriallizers import PreRegisterSerializer, RegisterSerializer, MiniCourseSerializer


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

            application_id = db.collection('applications').document().id
            message = (f"#application\n\n"
                       f"🚀 <b>Новая запись на мастер-класс по нейросетям!</b>\n\n"
                       f"ℹ️ ID: {application_id}\n"
                       f"👤 Имя: {name}\n"
                       f"📞 Телефон: {phone}\n"
                       f"📧 Почта: {email}\n"
                       f"✈️ Телеграм: {telegram if telegram else 'Не указан'}\n"
                       f"🧠 Деятельность: {'Не указана' if len(activities) == 0 else ', '.join(activities)}\n\n"
                       f"📄 Форма: Предзапись")
            await send_message_to_admins(message)
            await write_application(application_id, name, phone, email, telegram, activities)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as error:
            error_trace = traceback.format_exc()
            logging.error(error, error_trace)
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RegisterView(APIView):
    async def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)

            data = serializer.validated_data
            (name,
             phone,
             email,
             telegram,
             activity,
             tariff,
             price,
             payment_method,
             payment_type) = (data['name'],
                              data['phone'],
                              data['email'],
                              data.get('telegram'),
                              data['activity'],
                              data['tariff'],
                              data['price'],
                              data['payment_method'],
                              data['payment_type'])

            enrollment_id = db.collection('enrollments').document().id
            message = (f"#enrollment\n\n"
                       f"🚀 <b>Новый клиент на курсах по нейросетям!</b>\n\n"
                       f"ℹ️ ID: {enrollment_id}\n"
                       f"👤 Имя: {name}\n"
                       f"📞 Телефон: {phone}\n"
                       f"📧 Почта: {email}\n"
                       f"✈️ Телеграм: {telegram if telegram else 'Не указан'}\n"
                       f"🧠 Деятельность: {activity if activity else 'Не указана'}\n"
                       f"⭐ Тариф: {tariff}\n"
                       f"🏦 Предоплата: {'Да' if payment_type == PaymentType.PREPAYMENT else 'Нет'}\n"
                       f"💱 Метод оплаты: {'PayPal' if payment_method == PaymentMethod.PAYPAL else 'ЮKassa'}\n"
                       f"💸 Сумма: {price}{'$' if payment_method == PaymentMethod.PAYPAL else '₽'}\n"
                       f"👁 Статус: Ожидание оплаты\n\n"
                       f"📄 Форма: Запись")
            await send_message_to_admins(message)

            if payment_method == PaymentMethod.YOOKASSA:
                payment = await create_payment(float(price), email, name, tariff)
                await write_enrollment(
                    id=enrollment_id,
                    name=name,
                    phone=phone,
                    email=email,
                    telegram=telegram,
                    activity=activity,
                    tariff=tariff,
                    amount=float(payment.get('amount').get('value')),
                    income_amount=float(0),
                    payment_id=payment.get('id'),
                    payment_method=payment_method,
                    payment_type=payment_type,
                    payment_status=PaymentStatus.PENDING,
                )

                return Response(
                    {
                        **serializer.data,
                        'confirmation_url': payment.get('confirmation').get('confirmation_url'),
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                await write_enrollment(
                    id=enrollment_id,
                    name=name,
                    phone=phone,
                    email=email,
                    telegram=telegram,
                    activity=activity,
                    tariff=tariff,
                    amount=float(price),
                    income_amount=float(0),
                    payment_id='',
                    payment_method=payment_method,
                    payment_type=payment_type,
                    payment_status=PaymentStatus.PENDING,
                )

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as error:
            error_trace = traceback.format_exc()
            logging.error(error, error_trace)
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MiniCourseView(APIView):
    async def post(self, request, *args, **kwargs):
        serializer = MiniCourseSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)

            data = serializer.validated_data
            (name,
             email,
             telegram,
             price,
             payment_method) = (data['name'],
                                data['email'],
                                data.get('telegram'),
                                data['price'],
                                data['payment_method'])

            mini_course_id = db.collection('mini_courses').document().id
            message = (f"#mini_course\n\n"
                       f"🚀 <b>Новый клиент на мини-курсе!</b>\n\n"
                       f"ℹ️ ID: {mini_course_id}\n"
                       f"👤 Имя: {name}\n"
                       f"📧 Почта: {email}\n"
                       f"✈️ Телеграм: {telegram if telegram else 'Не указан'}\n"
                       f"💱 Метод оплаты: {'PayPal' if payment_method == PaymentMethod.PAYPAL else 'ЮKassa'}\n"
                       f"💸 Сумма: {price}{'$' if payment_method == PaymentMethod.PAYPAL else '₽'}\n"
                       f"👁 Статус: Ожидание оплаты\n\n"
                       f"📄 Форма: Запись")
            await send_message_to_admins(message)

            if payment_method == PaymentMethod.YOOKASSA:
                payment = await create_payment(float(price), email, name, TariffType.MINI)
                await write_mini_course(
                    id=mini_course_id,
                    name=name,
                    email=email,
                    telegram=telegram,
                    amount=float(payment.get('amount').get('value')),
                    income_amount=float(0),
                    payment_id=payment.get('id'),
                    payment_method=payment_method,
                    payment_status=PaymentStatus.PENDING,
                )

                return Response(
                    {
                        **serializer.data,
                        'confirmation_url': payment.get('confirmation').get('confirmation_url'),
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                await write_mini_course(
                    id=mini_course_id,
                    name=name,
                    email=email,
                    telegram=telegram,
                    amount=float(price),
                    income_amount=float(0),
                    payment_id='',
                    payment_method=payment_method,
                    payment_status=PaymentStatus.PENDING,
                )

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as error:
            error_trace = traceback.format_exc()
            logging.error(error, error_trace)
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
