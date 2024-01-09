from adrf.serializers import Serializer
from rest_framework import serializers


class PreRegisterSerializer(Serializer):
    # Example: Roman Danilov
    name = serializers.CharField(min_length=2, max_length=50)
    # Example: +1 (650) 642-1617
    phone = serializers.CharField(min_length=10, max_length=20)
    # Example: me@romandanilov.com
    email = serializers.EmailField()
    # Example: @roman_danilov
    telegram = serializers.CharField(min_length=6, max_length=33)
    # Example: ['Контент-менеджер', 'Дизайнер']
    activities = serializers.ListField(child=serializers.CharField())
