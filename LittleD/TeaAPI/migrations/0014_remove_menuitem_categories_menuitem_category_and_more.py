# Generated by Django 5.0.1 on 2024-10-23 16:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeaAPI', '0013_alter_cart_unique_together_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='categories',
        ),
        migrations.AddField(
            model_name='menuitem',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='TeaAPI.category'),
        ),
        migrations.DeleteModel(
            name='MenuitemCategory',
        ),
    ]
