import random
from datetime import timedelta

from django.db import models
from django.utils.timezone import now, localdate

from shop.models.product import Product
from shop.models.user import User


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('paid', 'Оплачен'),
        ('shipped', 'Отправлен'),
        ('completed', 'Завершен'),
        ('canceled', 'Отменен'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    delivery_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_delivery_date(self):
        random_days = random.randint(1, 7)
        self.delivery_date = now() + timedelta(days=random_days, hours=random.randint(9, 18))
        self.save()

    def check_and_update_paid_status(self):
        if self.status == 'paid' and (self.delivery_date - localdate()).days <= 2:
            self.status = 'shipped'
            self.save()

    def check_and_update_shipped_status(self):
        if self.status == 'shipped' and self.delivery_date == localdate():
            self.status = 'completed'
            self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
