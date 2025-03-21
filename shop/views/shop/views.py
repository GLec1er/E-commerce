import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from shop.forms import ProductForm, SellerProfileForm
from shop.models import SellerProfile, Basket, BasketItem, Order, OrderItem
from shop.models.product import Product


logger = logging.getLogger('shop')


class DashboardView(ListView):
    model = Product
    template_name = 'shop/dashboard.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        store = SellerProfile.objects.filter(user_id=self.request.user.id).first()
        logger.debug(f"Fetching products for store: {store.id if store else 'None'}")
        return Product.objects.filter(is_active=True).exclude(owner=store)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        return get_object_or_404(Product, id=self.kwargs['product_id'])


class SellerProfileView(DetailView):
    model = SellerProfile
    template_name = 'user/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        """Возвращает профиль продавца, если он существует, иначе None."""
        try:
            return self.request.user.seller_profile
        except ObjectDoesNotExist:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Проверяем, есть ли у пользователя профиль продавца
        profile = self.get_object()
        context['profile'] = profile
        context['user'] = self.request.user
        context['is_sealer'] = self.request.user.is_sealer

        # Если есть профиль продавца, загружаем товары
        if profile:
            products = Product.objects.filter(owner=profile)
            context['products'] = products
        else:
            context['products'] = None

        return context


class SellerProfileEditView(UpdateView):
    model = SellerProfile
    form_class = SellerProfileForm
    template_name = 'shop/profile_edit.html'
    success_url = reverse_lazy('user:profile')

    def get_object(self, queryset=None):
        return self.request.user.seller_profile


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product_form.html'
    success_url = reverse_lazy('user:profile')

    def form_valid(self, form):
        form.instance.owner = self.request.user.seller_profile
        logger.info(f"Product created: {form.instance.name}")
        return super().form_valid(form)


class ProductEditView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product_form.html'
    success_url = reverse_lazy('user:profile')

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user.seller_profile)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'shop/product_delete.html'
    success_url = reverse_lazy('user:profile')

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user.seller_profile)


# Функционал корзины
def basket_view(request):
    basket, _ = Basket.objects.get_or_create(user=request.user)

    basket_items = basket.basketitem_set.select_related('product', 'product__discount').all()
    total_price = sum(item.get_total_price() for item in basket_items)

    return render(
        request,
        'shop/basket.html',
        {
            'basket': basket,
            'basket_items': basket_items,
            'total_price': total_price,
        },
    )


@method_decorator(csrf_exempt, name='dispatch')
class BasketView(LoginRequiredMixin, View):
    """API-контроллер для управления корзиной"""

    def get(self, request, product_id):
        """Получение текущего количества товара в корзине"""
        product = get_object_or_404(Product, id=product_id)
        basket = Basket.objects.filter(user=request.user).first()

        if not basket:
            logger.warning(f"Basket not found for user: {request.user.id}")
            return JsonResponse({"quantity": 0})

        item = BasketItem.objects.filter(basket=basket, product=product).first()
        logger.debug(f"Fetching quantity for product {product.id}: {item.quantity if item else 0}")
        return JsonResponse({"quantity": item.quantity if item else 0})

    def post(self, request, product_id):
        """Добавление товара в корзину"""
        product = get_object_or_404(Product, id=product_id)
        basket, created = Basket.objects.get_or_create(user=request.user)
        item, item_created = BasketItem.objects.get_or_create(basket=basket, product=product)

        if not item_created:
            item.quantity += 1
            item.save()
            logger.info(f"Product {product.id} quantity updated in basket for user {request.user.id}")
        else:
            logger.info(f"Product {product.id} added to basket for user {request.user.id}")

        return JsonResponse({"quantity": item.quantity})

    def delete(self, request, product_id):
        """Удаление товара из корзины (уменьшение количества)"""
        product = get_object_or_404(Product, id=product_id)
        basket = Basket.objects.filter(user=request.user).first()

        if not basket:
            logger.warning(f"Basket not found for user: {request.user.id}")
            return JsonResponse({"quantity": 0})

        item = BasketItem.objects.filter(basket=basket, product=product).first()

        if not item:
            logger.warning(f"Product {product.id} not found in basket for user {request.user.id}")
            return JsonResponse({"quantity": 0})

        if item.quantity > 1:
            item.quantity -= 1
            item.save()
            logger.info(f"Product {product.id} quantity decreased in basket for user {request.user.id}")
        else:
            item.delete()
            logger.info(f"Product {product.id} removed from basket for user {request.user.id}")

        return JsonResponse({"quantity": item.quantity if item.quantity > 0 else 0})


# Orders
@login_required
def create_order(request):
    basket = Basket.objects.get(user=request.user)
    basket_items = basket.basketitem_set.all()

    if not basket_items:
        logger.info(f"User {request.user.id} tried to create order with empty basket.")
        return redirect('shop:basket')  # Если корзина пустая, возвращаем пользователя обратно

    # Создаём заказ
    order = Order.objects.create(user=request.user)
    logger.info(f"Order created for user {request.user.id}, order id: {order.id}")

    # Переносим товары из корзины в заказ
    for item in basket_items:
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        logger.debug(f"Added product {item.product.id} to order {order.id}")

    # Очищаем корзину
    basket_items.delete()

    logger.info(f"Basket cleared for user {request.user.id} after order creation.")
    return redirect('shop:orders')  # После оформления заказа переходим на страницу заказов


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("orderitem_set__product")

    for order in orders:
        order.check_and_update_paid_status()
        order.check_and_update_shipped_status()

    return render(request, "shop/orders.html", {"orders": orders})


@csrf_exempt
def pay_order(request, order_id):
    """Оплата заказа с установкой даты доставки."""
    order = get_object_or_404(Order, id=order_id)

    if order.status == "pending":
        order.status = "paid"
        order.set_delivery_date()
        return JsonResponse({"status": "paid", "delivery_date": order.delivery_date.strftime("%d.%m.%Y %H:%M")})

    return JsonResponse({"error": "Order cannot be paid"}, status=400)


@csrf_exempt
def cancel_order(request, order_id):
    """Отмена заказа."""
    order = get_object_or_404(Order, id=order_id)

    if order.status in ["pending", "paid"]:
        order.status = "canceled"
        order.save()
        return JsonResponse({"status": "canceled"})

    return JsonResponse({"error": "Cannot cancel this order"}, status=400)


@csrf_exempt
def delete_order(request, order_id):
    """Удаление заказа."""
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return JsonResponse({"status": "deleted"})
