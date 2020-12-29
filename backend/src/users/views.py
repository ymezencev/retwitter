from django.contrib.auth import get_user_model
from django.db.models import F
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from core.decorators import paginate
from users.models import Following
from users.permissions import IsOwnerOrStaffOrReadOnly
from users.serializers import UserPersonalInfoDetailSerializer, \
    UserFollowingListSerializer, UserFollowersListSerializer, \
    FollowSerializer, UnfollowSerializer


User = get_user_model()


class UserPersonalInfoDetailView(RetrieveUpdateAPIView,
                                 viewsets.GenericViewSet):
    """Отображаем и редактируем информацию о профиле пользователя"""
    lookup_value_regex = '\d+'
    queryset = User.objects.filter(is_active=True).annotate(owner_id=F('id'))
    serializer_class = UserPersonalInfoDetailSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]


class FollowingView(viewsets.ViewSet, viewsets.GenericViewSet):
    """
    Подписки пользователей друг на друга
    """
    pagination_class = PageNumberPagination
    queryset = Following.objects.all()

    @paginate
    @action(detail=True, methods=['get'], name='Get who user follows',
            serializer_class=UserFollowingListSerializer)
    def following(self, request, pk=None):
        """Список на кого подписна пользователь"""
        queryset = Following.objects.filter(user_id=pk).\
            select_related('following_user')
        return queryset

    @paginate
    @action(detail=True, methods=['get'], name='Get who follows user',
            serializer_class=UserFollowersListSerializer)
    def followers(self, request, pk=None):
        """Список кто подписан на пользоватлея"""
        queryset = Following.objects.filter(following_user_id=pk). \
            select_related('following_user')
        return queryset

    @action(detail=False, methods=['post'], name='Follow user',
            serializer_class=FollowSerializer)
    def follow(self, request):
        """Подписка текущего пользователя на другого"""
        serializer = self.get_serializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['post'], name='Unfollow user',
            serializer_class=UnfollowSerializer)
    def unfollow(self, request):
        """Отписаться от пользователя"""
        serializer = self.get_serializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
