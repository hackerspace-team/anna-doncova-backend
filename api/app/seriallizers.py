from rest_framework import serializers


class PreRegisterSerializer(serializers.Serializer):
    # Example: Roman Danilov
    name = serializers.CharField(min_length=2, max_length=50)
    # Example: +1 (650) 642-1617
    phone = serializers.CharField(min_length=10, max_length=20)
    # Example: me@romandanilov.com
    email = serializers.EmailField()
    # Example: ['Контент-менеджер', 'Дизайнер']
    activities = serializers.ListField(child=serializers.CharField())
