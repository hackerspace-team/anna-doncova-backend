from adrf.serializers import Serializer
from rest_framework import serializers

from app.models.enrollment import PaymentMethod, TariffType, PaymentType


class PreRegisterSerializer(Serializer):
    # Example: Roman Danilov
    name = serializers.CharField(min_length=2, max_length=50)
    # Example: +1 (650) 642-1617
    phone = serializers.CharField(min_length=10, max_length=20)
    # Example: me@romandanilov.com
    email = serializers.EmailField()
    # Example: @roman_danilov
    telegram = serializers.CharField(required=False, min_length=6, max_length=33)
    # Example: ['Контент-менеджер', 'Дизайнер']
    activities = serializers.ListField(child=serializers.CharField())


class RegisterSerializer(Serializer):
    # Example: Roman Danilov
    name = serializers.CharField(min_length=2, max_length=50)
    # Example: +1 (650) 642-1617
    phone = serializers.CharField(min_length=10, max_length=20)
    # Example: me@romandanilov.com
    email = serializers.EmailField()
    # Example: @roman_danilov
    telegram = serializers.CharField(required=False, min_length=6, max_length=33)
    # Example: Дизайнер
    activity = serializers.CharField(required=False)
    # Example: STANDARD
    tariff = serializers.ChoiceField([TariffType.STANDARD, TariffType.VIP, TariffType.PLATINUM])
    # Example: 29900
    price = serializers.IntegerField()
    # Example: YOOKASSA
    payment_method = serializers.ChoiceField([PaymentMethod.YOOKASSA, PaymentMethod.PAYPAL])
    # Example: FULL_PAYMENT
    payment_type = serializers.ChoiceField([PaymentType.PREPAYMENT, PaymentType.FULL_PAYMENT])
