from rest_framework.permissions import BasePermission


class RaisePermission(BasePermission):
    """Базовое право."""

    def has_permission(self, request, view):
        """Если не был описан метод."""
        return False


# Схема преобразования типов запросов в методы для обработки
ACTION_MAP = {
    'patch': 'partial_update',
    'put': 'update',
    'delete': 'destroy',
    'get': 'retrieve',
    'post': 'create',
}


class PermissionsByActionMixin:
    """Allows to define 'permission_classes' for specific action using permissions_by_action attribute."""

    @property
    def permissions_by_action(self):
        raise NotImplementedError('You must specify permissions_by_action attribute')

    def get_permissions(self):
        # определение метода для обработки
        method = self.request.method.lower()
        self.action = ACTION_MAP.get(method)
        permissions = self.permissions_by_action.get(self.action, [RaisePermission])
        if not isinstance(permissions, list):
            permissions = [permissions]
        return [permission() for permission in permissions]
