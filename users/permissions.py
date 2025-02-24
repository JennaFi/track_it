from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Moderator Permissions"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Moderator').exists()


class IsOwner(BasePermission):
    """Owner Permissions"""

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False


class IsUser(BasePermission):
    """Basic User Permissions"""

    def has_permission(self, request, view):
        return request.user.is_authenticated
