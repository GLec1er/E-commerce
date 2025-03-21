from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Логин пользователя и сохранение токенов в cookies."""
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Устанавливаем куки
        response = Response({"message": "Успешный вход"})
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            samesite="Lax",
            secure=True,
            max_age=15 * 60,
        )
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            samesite="Lax",
            secure=True,
            max_age=15 * 60,
        )

        return response


class LogoutView(APIView):
    def post(self, request):
        """Логаут - удаление cookies"""
        response = Response({"message": "Выход выполнен"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


class RefreshTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Обновление access-токена через refresh-токен из cookies."""
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response({"error": "Токен отсутствует"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
        except Exception:
            return Response({"error": "Недействительный токен"}, status=status.HTTP_401_UNAUTHORIZED)

        response = Response({"message": "Токен обновлён"})
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            samesite="Lax",
            secure=True,
            max_age=15 * 60,
        )

        return response
