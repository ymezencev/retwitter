from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from users.forms import CustomUserCreationForm, CustomUserChangeForm

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    """Редактирование основных данных пользователя в админке"""
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['username', 'name', 'email', 'is_staff']
    fieldsets = (
        ('User', {'fields': ('username', 'name', 'email')}),
        ('Info', {'fields': ('avatar', 'header', 'description', 'location',
                             'site',)}),
        ('Personal info', {'fields': ('first_name', 'last_name',
                                      'phone_number', 'date_of_birth',
                                      'gender', 'country',)}),
        ('Permissions', {'fields': ('is_staff',)}),
    )


admin.site.register(User, CustomUserAdmin)
