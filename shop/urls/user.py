from django.urls import path

from shop.views.shop.views import (
    SellerProfileView,
    SellerProfileEditView,
    ProductCreateView,
    ProductEditView,
    ProductDeleteView,
)
from shop.views.user import views
from shop.views.user.views import (
    RegisterView,
    login_view,
    logout_view,
    home,
    ProductUserDetailView,
    ShopCreateView,
    DiscountCreateView,
)

USER_URL_PATTERNS = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home, name='home'),
    path('profile/', SellerProfileView.as_view(), name='profile'),
    path('profile/edit/', SellerProfileEditView.as_view(), name='profile_edit'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:product_id>/', ProductUserDetailView.as_view(), name='product_detail'),
    path('product/<int:pk>/edit/', ProductEditView.as_view(), name='product_edit'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('create_shop/', ShopCreateView.as_view(), name='create_shop'),
    path('delete_shop/', views.delete_shop, name='delete_shop'),
    path('product/<int:product_id>/make_discount/', DiscountCreateView.as_view(), name='discount'),
]
