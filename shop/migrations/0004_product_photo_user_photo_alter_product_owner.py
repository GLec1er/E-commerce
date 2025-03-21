# Generated by Django 5.1.6 on 2025-02-22 19:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0003_alter_user_options_user_phone_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="photo",
            field=models.ImageField(
                blank=True,
                help_text="Upload a product photo.",
                null=True,
                upload_to="product_photos/",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="photo",
            field=models.ImageField(
                blank=True,
                help_text="Upload a profile photo.",
                null=True,
                upload_to="user_photos/",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="owner",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="shop.sellerprofile"),
        ),
    ]
