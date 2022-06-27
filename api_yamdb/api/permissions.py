from rest_framework import permissions
from reviews.models import ROLE_MODERATOR, ROLE_ADMIN


class MyBasePermission(permissions.BasePermission):
    message = 'Вы не обладаете достаточными правами для данной операции!'


class IsReadOnly(MyBasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )


class IsModerator(MyBasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and request.user.role == ROLE_MODERATOR
        )


class IsAdmin(MyBasePermission):

    def has_object_permission(self, request, view, obj):
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


class IsOwner(permissions.BasePermission):
    message = 'Вы не являетесь владельцем для данной операции!'

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated
            and obj.username == request.user
        )