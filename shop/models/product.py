from django.db import models
from django.utils import timezone

from shop.constans import COLOR_CHOICES, MATERIAL_CHOICES
from shop.models import SellerProfile


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    logo = models.ImageField(upload_to="brand_logos/", null=True, blank=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Discount(models.Model):
    DISCOUNT_TYPES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed amount'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    value = models.DecimalField(max_digits=5, decimal_places=2, help_text="The discount value")
    start_date = models.DateField()
    end_date = models.DateField()

    # Связь скидки с категорией
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name="discounts")

    # Связь скидки с конкретным продуктом
    product = models.ForeignKey('Product', null=True, blank=True, on_delete=models.SET_NULL, related_name="discounts")

    def apply_discount(self, price):
        if self.discount_type == 'percentage':
            return price - (price * self.value / 100)
        elif self.discount_type == 'fixed':
            return price - self.value
        return price

    def is_active(self):
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date

    def __str__(self):
        return f"{self.name} - {self.discount_type} - {self.value}%"


# Товар
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(SellerProfile, on_delete=models.CASCADE)
    photo = models.ImageField(
        upload_to='product_photos/',
        null=True,
        blank=True,
        help_text="Upload a product photo."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    quantity_in_stock = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    color = models.CharField(max_length=50, choices=COLOR_CHOICES, blank=True, null=True)
    material = models.CharField(max_length=100, choices=MATERIAL_CHOICES, blank=True, null=True)

    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL, related_name="products")

    def __str__(self):
        return self.name

    def get_discounted_price(self):
        if self.discount:
            return self.discount.apply_discount(self.price)
        return self.price
