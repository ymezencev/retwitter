from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.data import COUNTRIES


class User(AbstractUser):
    """Модель профиль пользователя. Расширение стандартной модели юзера"""
    GENDER_CHOICES = (('male', 'Male'), ('female', 'Female'))

    username = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=15, default=username)

    email = models.EmailField(unique=True)

    avatar = models.ImageField(upload_to='uploads/avatar',
                               blank=True, null=True)
    header = models.ImageField(upload_to='uploads/headers',
                               blank=True, null=True)
    description = models.TextField(max_length=160, null=True, blank=True)

    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES,
                              null=True, blank=True)
    country = models.CharField(max_length=30,
                               choices=sorted(COUNTRIES.items()))
    location = models.CharField(max_length=20, blank=True, null=True)
    site = models.URLField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f'@{self.username}'
