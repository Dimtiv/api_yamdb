from rest_framework import permissions

from api.plug import setFakeUserToRequest
from reviews.models import User, ROLE_MODERATOR, ROLE_ADMIN


class OwnerOrReadOnly(permissions.BasePermission):
    message = 'Вы не обладаете достаточными правами для данной операции!'

    def has_permission(self, request, view):
        # TODO убрать заглушку
        setFakeUserToRequest(request)
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # TODO убрать заглушку
        setFakeUserToRequest(request)
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class IsModerator(permissions.BasePermission):
    message = 'Вы не обладаете достаточными правами для данной операции!'

    def has_permission(self, request, view):
        # TODO убрать заглушку
        setFakeUserToRequest(request)
        print(request.user.role)
        return bool(request.user and request.user.role == ROLE_MODERATOR)


class IsAdmin(permissions.BasePermission):
    message = 'Вы не обладаете достаточными правами для данной операции!'

    def has_permission(self, request, view):
        # TODO убрать заглушку
        setFakeUserToRequest(request)
        return bool(request.user and request.user.role == ROLE_ADMIN)
