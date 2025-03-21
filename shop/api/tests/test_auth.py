from django.urls import reverse
from rest_framework import status

from .base import BaseAPITestCase


class AuthAPITestCase(BaseAPITestCase):
    """
    Тесты для аутентификации пользователей.

    Тесты проверяют:
    - успешную аутентификацию пользователя
    - неуспешную аутентификацию с неверными учетными данными
    - выход из системы
    - обновление токена
    """

    def test_login_success(self):
        """Тест успешной аутентификации пользователя."""
        url = reverse('api:login')
        response = self.client.post(url, {'username': 'testuser', 'password': 'testpass123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.cookies)
        self.assertIn('refresh_token', response.cookies)

    def test_login_invalid_credentials(self):
        """Тест неуспешной аутентификации с неверными учетными данными."""
        url = reverse('api:login')
        response = self.client.post(url, {'username': 'testuser', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_success(self):
        """Тест выхода из системы."""
        self.authenticate_user()
        url = reverse('api:logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_unauthorized(self):
        """Тест выхода из системы для неавторизованного пользователя."""
        url = reverse('api:logout')
        response = self.client.post(url)
        response.delete_cookie('access_token')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh_token_success(self):
        """Тест обновления токена."""
        # 1. Получаем refresh token
        login_url = reverse('api:login')
        login_response = self.client.post(login_url, {'username': 'testuser', 'password': 'testpass123'})

        # Проверяем, что логин успешен и есть куки с токенами
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh_token', login_response.cookies)

        # 2. Получаем refresh_token из куки
        refresh_token = login_response.cookies['refresh_token'].value

        # 3. Отправляем refresh_token в теле запроса
        refresh_url = reverse('api:token_refresh')
        response = self.client.post(refresh_url, {'refresh_token': refresh_token})

        # 4. Проверяем, что новый access_token получен
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.cookies)

    def test_refresh_token_invalid(self):
        """Тест обновления токена с недействительным refresh_token."""
        url = reverse('api:token_refresh')
        response = self.client.post(url, {'refresh_token': 'invalid_token'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
