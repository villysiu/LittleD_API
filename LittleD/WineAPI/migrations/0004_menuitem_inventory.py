# Generated by Django 5.0 on 2024-01-01 21:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WineAPI', '0003_orderitem_line_total_orderitem_unit_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='inventory',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(1000)]),
        ),
    ]
