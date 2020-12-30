from django.contrib.auth import get_user_model
from django.db.models import F
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, GenericViewSet

from core.decorators import paginate
from users.models import Following
from users.permissions import IsOwnerOrStaffOrReadOnly
from users.serializers import UserPersonalInfoDetailSerializer, \
    UserFollowingListSerializer, UserFollowersListSerializer, \
    FollowSerializer, UnfollowSerializer, ShortUserInfoSerializer

User = get_user_model()


class UsersListView(ListModelMixin, GenericViewSet):
    """Список пользователей с краткой информацией"""
    queryset = User.objects.filter(is_active=True)
    serializer_class = ShortUserInfoSerializer
    pagination_class = PageNumberPagination


class UserPersonalInfoDetailView(RetrieveUpdateAPIView, GenericViewSet):
    """Отображаем и редактируем информацию о профиле пользователя"""
    lookup_value_regex = '\d+'
    queryset = User.objects.filter(is_active=True).annotate(owner_id=F('id'))
    serializer_class = UserPersonalInfoDetailSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]


class FollowingView(ViewSet, GenericViewSet):
    """
    Подписки пользователей друг на друга
    """
    pagination_class = PageNumberPagination
    queryset = Following.objects.all()

    @paginate
    @action(detail=True, methods=['get'], name='Get who user follows',
            serializer_class=UserFollowingListSerializer)
    def following(self, request, pk=None):
        """Список на кого подписн пользователь"""
        queryset = Following.objects.filter(user_id=pk).values(
            'following_user_id', username=F('following_user__username'),
            name=F('following_user__name'), avatar=F('following_user__avatar')
        ).order_by('following_user__username')
        return queryset

    @paginate
    @action(detail=True, methods=['get'], name='Get who follows user',
            serializer_class=UserFollowersListSerializer)
    def followers(self, request, pk=None):
        """Список кто подписан на пользователя"""
        queryset = Following.objects.filter(following_user_id=pk).values(
            'user_id', username=F('user__username'), name=F('user__name'),
            avatar=F('user__avatar')).order_by('user__username')
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
