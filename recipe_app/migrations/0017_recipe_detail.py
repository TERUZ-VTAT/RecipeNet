# Generated by Django 5.1.4 on 2024-12-14 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_app', '0016_alter_recipe_recipe_image_favorites'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='detail',
            field=models.TextField(default='', verbose_name='detail'),
            preserve_default=False,
        ),
    ]
