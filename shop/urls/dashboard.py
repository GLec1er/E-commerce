from django.urls import path

from shop.views.shop import views
from shop.views.shop.views import (
    DashboardView,
    ProductDetailView,
    BasketView,
)


SHOP_URL_PATTERNS = [
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail_user'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('basket/', views.basket_view, name='basket'),
    path('basket/<int:product_id>/', BasketView.as_view(), name='basket_action'),
    path('orders/', views.order_list, name='orders'),
    path('create-order/', views.create_order, name='create_order'),
    path("orders/<int:order_id>/pay/", views.pay_order, name="pay_order"),
    path('orders/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('orders/<int:order_id>/delete/', views.delete_order, name='delete_order'),
]
