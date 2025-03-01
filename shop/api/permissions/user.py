from rest_framework import permissions


class IsAdminOrOwner(permissions.BasePermission):
    """
    Разрешение, которое позволяет доступ только администраторам
    или владельцам объекта.
    """

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        return obj == request.user
