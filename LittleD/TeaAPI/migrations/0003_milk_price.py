# Generated by Django 5.0.1 on 2024-02-01 18:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeaAPI', '0002_alter_orderitem_unique_together_orderitem_milk_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='milk',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
