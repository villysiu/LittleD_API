# Generated by Django 5.0 on 2024-01-04 01:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WineAPI', '0006_remove_order_status_order_order_status'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderStatus',
        ),
    ]
