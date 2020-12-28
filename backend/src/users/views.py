from django.contrib.auth import get_user_model
from django.db.models import F
from rest_framework import viewsets
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin

from users.permissions import IsOwnerOrStaffOrReadOnly
from users.serializers import UserPersonalInfoDetailSerializer


User = get_user_model()


class UserPersonalInfoDetailView(RetrieveModelMixin, UpdateModelMixin,
                                 viewsets.GenericViewSet):
    """Отображаем и редактируем информацию о профиле пользователя"""
    queryset = User.objects.all().annotate(owner_id=F('id'))
    serializer_class = UserPersonalInfoDetailSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]

