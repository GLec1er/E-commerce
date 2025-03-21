from django.urls import reverse
from rest_framework import status

from .base import BaseAPITestCase


class ProductAPITestCase(BaseAPITestCase):
    """
    Тесты для продуктов.

    Тесты проверяют:
    - создание продукта
    - список продуктов
    - детали продукта
    - обновление продукта
    - удаление продукта
    """
    def setUp(self):
        super().setUp()
        self.product_data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': '100.00',
            'owner': self.seller.id
        }

    def test_create_product_as_seller(self):
        """Тест создания продукта для продавца."""
        self.authenticate_user(self.user)
        url = reverse('api:product:product-list')
        response = self.client.post(url, self.product_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.product_data['name'])

    def test_create_product_as_regular_user(self):
        """Тест создания продукта для обычного пользователя."""
        self.authenticate_user()
        url = reverse('api:product:product-list')
        response = self.client.post(url, self.product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_products(self):
        """Тест получения списка продуктов."""
        # Создаем продукт через продавца
        self.authenticate_user(self.user)
        url = reverse('api:product:product-list')
        self.client.post(url, self.product_data)

        # Проверяем список продуктов
        self.client.credentials()
        url_list = reverse('api:product:list')
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_product(self):
        """Тест получения деталей продукта."""
        # Создаем продукт
        self.authenticate_user(self.user)
        url = reverse('api:product:product-list')
        create_response = self.client.post(url, self.product_data)
        product_id = create_response.data['id']

        # Получаем детали продукта
        self.client.credentials()
        detail_url = reverse('api:product:product-detail', kwargs={'pk': product_id})
        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product_data['name'])

    def test_update_product(self):
        """Тест обновления продукта."""
        # Создаем продукт
        self.authenticate_user(self.user)
        url = reverse('api:product:product-list')
        create_response = self.client.post(url, self.product_data)
        product_id = create_response.data['id']

        # Обновляем продукт
        update_data = {'name': 'Updated Product'}
        detail_url = reverse('api:product:product-detail', kwargs={'pk': product_id})
        response = self.client.patch(detail_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], update_data['name'])

    def test_delete_product(self):
        """Тест удаления продукта."""
        # Создаем продукт
        self.authenticate_user(self.user)
        url = reverse('api:product:product-list')
        create_response = self.client.post(url, self.product_data)
        product_id = create_response.data['id']

        # Удаляем продукт
        detail_url = reverse('api:product:product-detail', kwargs={'pk': product_id})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
