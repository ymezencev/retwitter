from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F, Q
from django_countries.data import COUNTRIES

from config import settings


class User(AbstractUser):
    """
    Модель профиль пользователя.
    Расширение стандартной модели юзера.
    """
    GENDER_CHOICES = (('male', 'Male'), ('female', 'Female'))

    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30)
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
                               choices=sorted(COUNTRIES.items()),
                               null=True, blank=True)
    location = models.CharField(max_length=20, blank=True, null=True)
    site = models.URLField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    def save(self, *args, **kwargs):
        is_creating = not self.pk

        if not self.name and is_creating:
            # При создании пользователя  name = username
            self.name = self.username
        super().save(*args, **kwargs)

    def __str__(self):
        return f'@{self.username}'


class Following(models.Model):
    """
    Модель для подписок пользователей друг на друга
    """
    user = models.ForeignKey(User, related_name='following',
                             on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name='followers',
                                       on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'following_user'],
                                    name='unique_followers'),
            models.CheckConstraint(check=~Q(user_id=F('following_user_id')),
                                   name='self_not_follow')
        ]

    def __str__(self):
        return f'{self.user_id} follows {self.following_user_id}'
