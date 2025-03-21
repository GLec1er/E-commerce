import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from rest_framework_simplejwt.tokens import RefreshToken

from shop.forms import CustomUserCreationForm, LoginForm, ShopForm, DiscountForm
from shop.models import Product, StoreName, SellerProfile
from shop.models.product import Discount

logger = logging.getLogger('shop')


# Регистрация
class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        logger.info(f"New user registration: {form.cleaned_data['username']}")
        return super().form_valid(form)


# Вход
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                logger.info(f"User {username} logged in successfully.")

                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                response = redirect('shop:dashboard')
                response.set_cookie(
                    key="access_token",
                    value=access_token,
                    httponly=True,
                    samesite="Lax",
                    secure=True,
                )
                response.set_cookie(
                    key="refresh_token",
                    value=str(refresh),
                    httponly=True,
                    samesite="Lax",
                    secure=True,
                )

                return response
            else:
                logger.warning(f"Failed login attempt for username: {username}")
                messages.error(request, 'Неверное имя пользователя или пароль.')
        else:
            logger.error("Login form contains errors.")
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = LoginForm()

    return render(request, 'user/login.html', {'form': form})


def logout_view(request):
    logger.info(f"User {request.user.username} logged out.")
    response = redirect('user:login')

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    logout(request)
    return response


def home(request):
    return render(
        request,
        'user/home.html',
    )


@login_required
def profile_view(request):
    return render(
        request,
        'user/profile.html',
        {'user': request.user},
    )


class ProductUserDetailView(DetailView):
    model = Product
    template_name = 'user/product_detail_user.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        return get_object_or_404(Product, id=self.kwargs['product_id'])


# Create a shop
class ShopCreateView(CreateView):
    model = StoreName
    form_class = ShopForm
    template_name = 'shop/create_shop.html'
    success_url = reverse_lazy('user:profile')

    def dispatch(self, request, *args, **kwargs):
        seller_profile = getattr(request.user, 'seller_profile', None)

        if seller_profile and StoreName.objects.filter(owner=seller_profile).exists():
            logger.warning(f"User {request.user.username} attempted to create a shop, but already has one.")
            messages.warning(request, "У вас уже есть магазин.")
            return redirect('user:profile')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        logger.info(f"Shop created successfully for user {self.request.user.username}.")
        form.save(user=self.request.user)
        messages.success(self.request, "Магазин успешно создан!")
        return redirect(self.success_url)

    def form_invalid(self, form):
        logger.error(f"Error creating shop for user {self.request.user.username}. Invalid form data.")
        messages.error(self.request, "Ошибка при создании магазина. Проверьте введённые данные.")
        return super().form_invalid(form)


class DiscountCreateView(CreateView):
    model = Discount
    form_class = DiscountForm
    template_name = 'shop/includes/discount.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        context['product'] = product
        return context

    def form_valid(self, form):
        # Получаем продукт, к которому привязывается скидка
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        # Сохраняем скидку с привязкой к продукту
        discount = form.save(commit=False)
        discount.product = product  # Привязываем скидку к продукту
        discount.save()

        # Обновляем продукт, чтобы он знал о скидке
        product.discount = discount
        product.save()

        # Перенаправляем на страницу продукта
        return redirect('user:product_detail', product_id=product.id)


@login_required
def delete_shop(request):
    if not request.user.is_sealer:
        logger.warning(f"User {request.user.username} attempted to delete a shop they don't own.")
        messages.error(request, "You don't have a shop to delete.")
        return redirect('user:profile')

    sealer_profile = get_object_or_404(SellerProfile, user=request.user)
    sealer_profile.store_name.delete()
    sealer_profile.delete()

    # Обновляем статус пользователя
    request.user.is_sealer = False
    request.user.save()

    logger.info(f"Shop for user {request.user.username} deleted successfully.")
    messages.success(request, "Your shop has been deleted successfully.")
    return redirect('user:profile')
