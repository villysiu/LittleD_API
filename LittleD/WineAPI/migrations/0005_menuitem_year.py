# Generated by Django 5.0 on 2023-12-28 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WineAPI', '0004_menuitem_description_menuitem_origin_menuitem_point_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='year',
            field=models.SmallIntegerField(default=2000),
            preserve_default=False,
        ),
    ]
