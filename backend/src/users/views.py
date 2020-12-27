from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated

from users.serializers import UserPersonalInfoDetailSerializer


User = get_user_model()


class UserPersonalInfoDetailView(RetrieveModelMixin, UpdateModelMixin,
                                 viewsets.GenericViewSet):
    """Отображаем и редактируем информацию о профиле пользователя"""
    queryset = User.objects.all()
    serializer_class = UserPersonalInfoDetailSerializer
    permission_classes = [IsAuthenticated]

