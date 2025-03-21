from rest_framework import serializers
from shop.models import BasketItem, Product
from shop.models.user import User


class BasketItemSerializer(serializers.ModelSerializer):
    """Сериализатор для корзины."""
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = BasketItem
        fields = [
            'id',
            'product',
            'product_name',
            'product_price',
            'quantity',
            'total_price',
        ]

    def get_total_price(self, obj):
        """Возвращает общую стоимость товара с учетом количества."""
        if isinstance(obj, dict):
            return obj.get('total_price', 0)
        return obj.get_total_price()
