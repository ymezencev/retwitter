from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """Форма для создания пользователя"""
    class Meta:
        model = User
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    """Форма для редактирования данных пользователя"""
    class Meta:
        model = User
        # fields = UserChangeForm.Meta.fields
        fields = ('username', 'name', 'email')
