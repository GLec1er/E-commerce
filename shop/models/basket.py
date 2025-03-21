from django.db import models

from shop.models.product import Product
from shop.models.user import User


# Корзина
class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='BasketItem')


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        """Возвращает цену товара с учетом скидки и количества."""
        if self.product.discount:
            product_price = self.product.get_discounted_price()
        product_price = self.product.price
        return product_price * self.quantity
