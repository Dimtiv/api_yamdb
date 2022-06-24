from rest_framework import permissions
from reviews.models import ROLE_MODERATOR, ROLE_ADMIN


class OwnerOrReadOnly(permissions.BasePermission):
    message = 'Вы не обладаете достаточными правами для данной операции!'

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsModerator(permissions.BasePermission):
    message = 'Вы не обладаете достаточными правами для данной операции!'

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated
            and request.user.role == ROLE_MODERATOR
        )


class IsAdmin(permissions.BasePermission):
    message = 'Вы не обладаете достаточными правами для данной операции!'

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated
            and (request.user.role == ROLE_ADMIN or request.user.is_staff)
        )
