# Generated by Django 5.1.3 on 2024-12-04 00:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_app', '0006_remove_recipe_recipe_id_recipe_recipe_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipesection',
            name='detail',
            field=models.TextField(verbose_name='detail'),
        ),
        migrations.AlterField(
            model_name='recipesection',
            name='index_num',
            field=models.IntegerField(verbose_name='index_num'),
        ),
        migrations.AlterField(
            model_name='recipesection',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe_app.recipe', verbose_name='recipe'),
        ),
    ]
