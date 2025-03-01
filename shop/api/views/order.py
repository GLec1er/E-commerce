from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from shop.api.serializers.order import OrderSerializer, OrderItemSerializer
from shop.models import Order, OrderItem


class OrderAPIView(generics.ListAPIView):
    """Получение всех заказов пользователя."""
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderProductAPIView(generics.ListAPIView):
    """Получение списка продуктов из конкретного заказа."""
    permission_classes = [IsAuthenticated]
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        order_id = self.kwargs.get("order_id")
        return OrderItem.objects.filter(order__id=order_id, order__user=self.request.user)
