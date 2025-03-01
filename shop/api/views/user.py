from rest_framework import mixins, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from shop.api.filters.user import UserListFilter
from shop.api.permissions.base import PermissionsByActionMixin
from shop.api.permissions.user import IsAdminOrOwner
from shop.api.serializers.user import UserSerializer
from shop.models.user import User


class UserAPIView(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    PermissionsByActionMixin,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permissions_by_action = {
        'create': IsAuthenticated,
        'retrieve': IsAdminOrOwner,
        'update': IsAuthenticated,
        'destroy': IsAdminOrOwner,
    }

    def perform_create(self, serializer):
        """Создание нового пользователя"""
        user = serializer.save()
        return user

    def perform_destroy(self, instance):
        """Удаление пользователя"""
        instance.delete()


class UserListView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrOwner]
    filterset_class = UserListFilter

    def get_queryset(self):
        return User.objects.all()
