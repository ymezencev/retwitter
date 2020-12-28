from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_auth.serializers import LoginSerializer as RestAuthLoginSerializer


User = get_user_model()


class UserLoginSerializer(RestAuthLoginSerializer):
    """Логин по username и password"""
    email = None


class UserDetailSerializer(serializers.ModelSerializer):
    """Личные данные пользователя"""
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'first_name', 'last_name',
                  'phone_number', 'date_of_birth', 'gender', 'country', ]


class UserPersonalInfoDetailSerializer(serializers.ModelSerializer):
    """Персональная информация для отображения в профиле пользователя"""

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'avatar', 'header', 'description',
                  'location', 'site']
        read_only_fields = ['id', 'username', 'name']
