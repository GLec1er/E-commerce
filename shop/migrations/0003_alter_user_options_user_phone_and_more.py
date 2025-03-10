# Generated by Django 5.1.6 on 2025-02-22 13:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("shop", "0002_storename_alter_sellerprofile_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={},
        ),
        migrations.AddField(
            model_name="user",
            name="phone",
            field=models.CharField(
                blank=True,
                help_text="Enter a valid phone number (e.g., +1234567890).",
                max_length=15,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Phone number must contain 10 to 15 digits and can start with '+'.",
                        regex="^\\+?\\d{10,15}$",
                    )
                ],
            ),
        ),
        migrations.AddConstraint(
            model_name="user",
            constraint=models.CheckConstraint(
                condition=models.Q(("phone__regex", "^\\+?\\d{10,15}$")),
                name="valid_phone_number",
            ),
        ),
    ]
