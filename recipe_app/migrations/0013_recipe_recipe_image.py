# Generated by Django 5.1.4 on 2024-12-06 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_app', '0012_recipe_public_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='recipe_image',
            field=models.ImageField(default='', upload_to='', verbose_name='recipe_image'),
            preserve_default=False,
        ),
    ]
