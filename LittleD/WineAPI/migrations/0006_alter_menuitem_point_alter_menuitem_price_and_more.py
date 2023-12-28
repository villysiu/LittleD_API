# Generated by Django 5.0 on 2023-12-28 22:43

import WineAPI.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WineAPI', '0005_menuitem_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='point',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='year',
            field=models.PositiveSmallIntegerField(validators=[WineAPI.models.MenuItem.year_validator]),
        ),
    ]
