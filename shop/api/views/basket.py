from rest_framework import viewsets, generics, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from shop.models import Basket, BasketItem, Product
from shop.api.serializers.basket import BasketItemSerializer


class BasketListView(generics.ListAPIView):
    """Получение всех товаров в корзине текущего пользователя."""

    serializer_class = BasketItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        basket, _ = Basket.objects.get_or_create(user=self.request.user)
        return BasketItem.objects.filter(basket=basket)


class BasketAPIView(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    """Добавление, обновление и удаление товаров из корзины."""

    permission_classes = [IsAuthenticated]
    serializer_class = BasketItemSerializer
    queryset = BasketItem.objects.select_related("basket", "product").all()

    def perform_create(self, request):
        """Добавление товара в корзину."""
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        product = get_object_or_404(Product, id=product_id)
        basket, _ = Basket.objects.get_or_create(user=request.user)
        basket_item, created = BasketItem.objects.get_or_create(basket=basket, product=product)

        if not created:
            basket_item.quantity += int(quantity)
        else:
            basket_item.quantity = int(quantity)

        basket_item.save()
        return Response(BasketItemSerializer(basket_item).data, status=status.HTTP_201_CREATED)

    def perform_update(self, request, pk=None):
        """Обновление количества товара в корзине."""
        basket_item = get_object_or_404(BasketItem, pk=pk, basket__user=request.user)
        quantity = request.data.get("quantity", 1)
        basket_item.quantity = int(quantity)
        basket_item.save()
        return Response(BasketItemSerializer(basket_item).data)

    def perform_destroy(self, request, pk=None):
        """Удаление товара из корзины."""
        basket_item = get_object_or_404(BasketItem, pk=pk, basket__user=request.user)
        basket_item.delete()
        return Response({"detail": "Товар удален из корзины."}, status=status.HTTP_204_NO_CONTENT)
