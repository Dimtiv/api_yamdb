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

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated
            and (request.user.role == ROLE_ADMIN or request.user.is_staff)
        )


class IsAdminForUserVievSet(MyBasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == ROLE_ADMIN or request.user.is_staff))


class IsAdminOrSelf(MyBasePermission):
    """
    Allow access to admin users or the user himself.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff or ROLE_ADMIN)

    def has_object_permission(self, request, view, obj):
        if request.user and (request.user.is_staff or request.user.role == ROLE_ADMIN):
            return True
        elif (request.user and type(obj) == type(request.user) and
              obj == request.user):
            return True
        return False


class IsOwner(MyBasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated
            and (obj == request.user
                 or 'author' in obj and obj.author == request.user)
        )