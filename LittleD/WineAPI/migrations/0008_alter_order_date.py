# Generated by Django 5.0.1 on 2024-01-23 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WineAPI', '0007_delete_orderstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
    ]