from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrStaffOrReadOnly(BasePermission):
    """
    Запрос от авторизованного пользователя или запрос на просмотр
    Создание, обновление, удаление доступно только для владельца
    """

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and (
                    obj.owner_id == request.user.id or request.user.is_staff)
        )
