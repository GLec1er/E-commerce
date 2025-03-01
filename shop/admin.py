from django.contrib import admin

from shop.models.basket import Basket, BasketItem
from shop.models.order import Order, OrderItem
from shop.models.product import Product, Category, Brand, Discount
from shop.models.seller import SellerProfile, StoreName
from shop.models.user import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_sealer', 'email')


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'store_name', 'rating')


@admin.register(StoreName)
class StoreNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'owner', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('owner', 'created_at')


class BasketItemInline(admin.TabularInline):
    model = BasketItem
    extra = 0
    fields = ('product', 'quantity')
    readonly_fields = ('product',)


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user',)
    inlines = [BasketItemInline]


@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ('basket', 'product', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_at')
    list_filter = ('status', 'created_at')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Discount)
