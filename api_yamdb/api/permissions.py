from rest_framework import permissions
from reviews.models import ROLE_MODERATOR, ROLE_ADMIN


class MyBasePermission(permissions.BasePermission):
    message = 'Вы не обладаете достаточными правами для данной операции!'


class IsReadOnly(MyBasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsModerator(MyBasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and request.user.role == ROLE_MODERATOR
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsAdmin(MyBasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and (request.user.role == ROLE_ADMIN or request.user.is_staff)
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsOwner(MyBasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated
            and (obj == request.user
                 or hasattr(obj, 'author') and obj.author == request.user)
        )
