from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from main import settings
from shop.api.urls import API_URL_PATTERNS
from shop.apps import ShopConfig
from shop.urls.dashboard import SHOP_URL_PATTERNS
from shop.urls.user import USER_URL_PATTERNS

schema_view = get_schema_view(
    openapi.Info(
        title="E-commerce API",
        default_version='v2',
        description="API documentation for E-commerce",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="grisha.lavrov.178@mail.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path('shop/', include((SHOP_URL_PATTERNS, ShopConfig.name), namespace='shop')),
    path('user/', include((USER_URL_PATTERNS, ShopConfig.name), namespace='user')),
    path('api/', include((API_URL_PATTERNS, ShopConfig.name), namespace='api')),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-docs'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
