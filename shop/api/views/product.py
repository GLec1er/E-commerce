from rest_framework import viewsets, mixins
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action

from shop.api.permissions.base import PermissionsByActionMixin
from shop.api.permissions.user import IsAdminOrOwner
from shop.api.serializers.product import ProductSerializer
from shop.models import Product, SellerProfile


class ProductAPIView(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    PermissionsByActionMixin,
):
    """API для работы с продуктами"""

    queryset = Product.objects.select_related('category', 'brand', 'discount', 'owner').all()
    serializer_class = ProductSerializer

    permissions_by_action = {
        'create': IsAuthenticated,
        'retrieve': IsAuthenticated,
        'update': IsAuthenticated,
        'destroy': IsAdminOrOwner,
    }

    def perform_create(self, serializer):
        """Метод создания продукта."""
        serializer.save()

    def perform_update(self, serializer):
        """Метод обновления продукта."""
        serializer.save()

    def perform_destroy(self, instance):
        """Метод удаления продукта."""
        instance.delete()

    @action(detail=True, methods=['get'])
    def discounted_price(self, request, pk=None):
        """Получение цены товара с учетом скидки."""
        product = self.get_object()
        return Response({'discounted_price': product.get_discounted_price()})


class ProductListView(ListAPIView):
    """API для получения списка всех продуктов."""

    queryset = Product.objects.select_related(
        'category',
        'brand',
        'discount',
        'owner',
    ).all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
