# Generated by Django 5.1.2 on 2024-10-21 05:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_product_discount'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='users_like',
            field=models.ManyToManyField(blank=True, null=True, related_name='users_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
