# from django.db import models
# from django.contrib.auth.models import AbstractUser
#
#
# # Пользователь
# class User(AbstractUser):
#     is_sealer = models.BooleanField(
#         default=False,
#         help_text='This user can to add your product',
#     )
#     email = models.EmailField(unique=True)
#     groups = models.ManyToManyField(
#         "auth.Group",
#         related_name="custom_user_set",
#         blank=True
#     )
#     user_permissions = models.ManyToManyField(
#         "auth.Permission",
#         related_name="custom_user_permissions_set",
#         blank=True
#     )
#
#     def __str__(self):
#         return self.username
#
#
# # Продавец
# class SellerProfile(models.Model):
#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         related_name="seller_profile"
#     )
#     store_name = models.CharField(max_length=255, unique=True)
#     description = models.TextField(blank=True, null=True)
#     rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.store_name
#
#
# # Товар
# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     owner = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.name
#
#
# # Корзина
# class Basket(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     products = models.ManyToManyField(Product, through='BasketItem')
#
#
# class BasketItem(models.Model):
#     basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#
#
# # Заказ
# class Order(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'В ожидании'),
#         ('paid', 'Оплачен'),
#         ('shipped', 'Отправлен'),
#         ('completed', 'Завершен'),
#         ('canceled', 'Отменен'),
#     ]
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     products = models.ManyToManyField(Product, through='OrderItem')
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#
# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#
