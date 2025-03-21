from django.db import models

from shop.models import User


class StoreName(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    logo = models.ImageField(upload_to='store_logos/', null=True, blank=True, help_text="Upload a store logos.")

    class Meta:
        verbose_name = "Store Name"
        verbose_name_plural = "Store Names"
        ordering = ["name"]

    def __str__(self):
        return self.name


class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="seller_profile")
    store_name = models.OneToOneField(
        StoreName, on_delete=models.SET_NULL, null=True, blank=True, related_name="seller_profile"
    )
    description = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Seller Profile"
        verbose_name_plural = "Seller Profiles"
        ordering = ["-created_at"]

    def __str__(self):
        return f'{self.user} - {self.store_name.name}'
