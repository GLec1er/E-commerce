from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        """Берем access-токен из cookies, если он есть"""
        access_token = request.COOKIES.get("access_token")
        if not access_token:
            return None  # Не аутентифицируем, если токена нет

        try:
            validated_token = self.get_validated_token(access_token)
            return self.get_user(validated_token), validated_token
        except AuthenticationFailed:
            return None  # Токен невалиден, но не кидаем ошибку, просто пропускаем
