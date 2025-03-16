# Пользователь
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_sealer = models.BooleanField(
        default=False,
        help_text='This user can to add your product',
    )
    phone = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        help_text="Enter a valid phone number (e.g., +1234567890).",
        validators=[
            RegexValidator(
                regex=r"^\+?\d{10,15}$", message="Phone number must contain 10 to 15 digits and can start with '+'."
            )
        ],
    )
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True, help_text="Upload a profile photo.")
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField("auth.Group", related_name="custom_user_set", blank=True)
    user_permissions = models.ManyToManyField("auth.Permission", related_name="custom_user_permissions_set", blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(phone__regex=r"^\+?\d{10,15}$"), name="valid_phone_number")
        ]

    def __str__(self):
        return self.username
