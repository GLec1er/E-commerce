from rest_framework import serializers

from shop.api.serializers.product import ProductSerializer
from shop.api.serializers.user import UserSerializer
from shop.models import Order, OrderItem


class BaseOrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "status",
            "delivery_date",
            "created_at",
            "updated_at",
        ]


class OrderSerializer(BaseOrderSerializer):
    products = ProductSerializer(many=True)

    class Meta(BaseOrderSerializer.Meta):
        fields = BaseOrderSerializer.Meta.fields + [
            "products"
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "order",
            "product",
            "quantity",
        ]
