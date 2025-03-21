from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse
from shop.models.seller import SellerProfile, StoreName
from shop.models.user import User


class BaseAPITestCase(APITestCase):
    """Базовый класс для тестирования API с предустановленными пользователями и вспомогательными методами."""

    def setUp(self):
        """Создание тестовых пользователей."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            is_sealer=True,
        )
        self.seller = SellerProfile.objects.create(
            user=self.user,
            store_name=StoreName.objects.create(name='Test Store'),
        )
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )

        # Проверка, что пользователи созданы
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(User.objects.filter(username='admin').exists())

    def get_access_token(self, username='testuser', password='testpass123'):
        """Получение токена авторизации."""
        url = reverse('api:login')
        response = self.client.post(url, {
            'username': username,
            'password': password
        })
        return response.cookies.get('access_token')

    def authenticate_user(self, user=None):
        """Аутентификация пользователя."""
        if user is None:
            user = self.user
        token = self.get_access_token(username=user.username)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def create_test_product(self, seller=None):
        """Создание тестового продукта."""
        if seller is None:
            seller = self.seller
        url = reverse('shop:product-list')
        data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': '100.00',
            'owner': seller.id
        }
        response = self.client.post(url, data)

        # Проверка, что продукт создан
        self.assertEqual(response.status_code, 201)
        self.assertTrue('id' in response.data)
        return response.data
