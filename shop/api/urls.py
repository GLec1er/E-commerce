from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shop.api.jwt.views import LoginView, LogoutView, RefreshTokenView
from shop.api.views.basket import BasketAPIView, BasketListView
from shop.api.views.order import OrderAPIView, OrderProductAPIView
from shop.api.views.product import ProductListView, ProductAPIView
from shop.api.views.user import UserAPIView, UserListView
from shop.apps import ShopConfig

user_router = DefaultRouter()
user_router.register(r'', UserAPIView, basename='user')


USER_URL_PATTERNS = [
    path('list', UserListView.as_view(), name='list'),
    path('', include(user_router.urls)),
]

product_router = DefaultRouter()
product_router.register(r'', ProductAPIView, basename='product')

PRODUCT_URL_PATTERNS = [
    path('list/', ProductListView.as_view(), name='list'),
    path('', include(product_router.urls)),
]

basket_router = DefaultRouter()
basket_router.register(r'', BasketAPIView, basename='basket')

BASKET_URL_PATTERNS = [
    path('list/', BasketListView.as_view(), name='list'),
    path('', include(basket_router.urls)),
]

ORDER_URL_PATTERNS = [
    path('list/', OrderAPIView.as_view(), name='list'),
    path('<int:order_id>/', OrderProductAPIView.as_view(), name='order'),
]

API_URL_PATTERNS = [
    path('user/', include((USER_URL_PATTERNS, ShopConfig.name), namespace='user')),
    path('product/', include((PRODUCT_URL_PATTERNS, ShopConfig.name), namespace='product')),
    path('basket/', include((BASKET_URL_PATTERNS, ShopConfig.name), namespace='basket')),
    path('order/', include((ORDER_URL_PATTERNS, ShopConfig.name), namespace='order')),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
]
