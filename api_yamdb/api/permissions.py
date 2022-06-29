from rest_framework import permissions
from reviews.models import ROLE_MODERATOR, ROLE_ADMIN


class MyBasePermission(permissions.BasePermission):
    message = 'Вы не обладаете достаточными правами для данной операции!'


class IsReadOnly(MyBasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
        )


class IsModerator(MyBasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and request.user.role == ROLE_MODERATOR
        )


class IsAdmin(MyBasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and (request.user.role == ROLE_ADMIN or request.user.is_staff)
        )


class IsOwner(MyBasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated
            and (obj == request.user
                 or 'author' in obj and obj.author == request.user)
        )
