from rest_framework import serializers

from shop.models import SellerProfile, StoreName
from shop.models.product import Category, Brand, Discount, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'is_active']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'description', 'country', 'logo']


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'name', 'discount_type', 'value', 'start_date', 'end_date']


class StoreNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreName
        fields = '__all__'


class OwnerSerializer(serializers.ModelSerializer):
    store_name = StoreNameSerializer()

    class Meta:
        model = SellerProfile
        fields = ['store_name', 'description', 'rating', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    discount = DiscountSerializer(read_only=True)
    owner = OwnerSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
