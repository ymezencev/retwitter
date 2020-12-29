from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_auth.serializers import LoginSerializer as RestAuthLoginSerializer
from rest_framework.generics import get_object_or_404

from users.models import Following

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
        read_only_fields = ['username', 'name']


class UserFollowingListSerializer(serializers.ModelSerializer):
    """На кого подписан пользователь"""
    following_user = UserPersonalInfoDetailSerializer(read_only=True)

    class Meta:
        model = Following
        fields = ("following_user",
                  "created_at")
        read_only_fields = ('following_user', 'created_at')


class UserFollowersListSerializer(serializers.ModelSerializer):
    """Подписчики пользователя"""
    user = UserPersonalInfoDetailSerializer(read_only=True)

    class Meta:
        model = Following
        fields = ("user",
                  "created_at")
        read_only_fields = ('user', 'created_at')


class FollowSerializer(serializers.ModelSerializer):
    """Подписка текущего пользователя на другого"""
    following_user_id = serializers.IntegerField()

    class Meta:
        model = Following
        fields = ['following_user_id']

    @transaction.atomic
    def save(self):
        user = self.context['request'].user
        following_user_id = self.validated_data['following_user_id']
        following_user_obj = get_object_or_404(User, id=following_user_id)
        if user == following_user_obj:
            return
        following = Following.objects.get_or_create(
            user=user, following_user=following_user_obj)
        # todo: add signal that user start following
        return following


class UnfollowSerializer(serializers.ModelSerializer):
    """Отписаться от пользователя"""
    unfollowing_user_id = serializers.IntegerField(source='following_user_id')

    class Meta:
        model = Following
        fields = ['unfollowing_user_id']

    @transaction.atomic
    def save(self):
        user = self.context['request'].user
        unfollowing_user_id = self.validated_data['following_user_id']
        unfollowing_user_obj = get_object_or_404(User, id=unfollowing_user_id)
        unfollowing = get_object_or_404(
            Following, user=user, following_user=unfollowing_user_obj).delete()
        # todo: add signal that user unfollowing
        return unfollowing
