from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserLoginSerializer(serializers.ModelSerializer):
    """Основные данные пользователя"""
    class Meta:
        model = User
        fields = ['username', 'password']


class UserDetailSerializer(serializers.ModelSerializer):
    """Основные данные пользователя"""
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'first_name', 'last_name',
                  'phone_number', 'date_of_birth', 'gender', 'country', ]
