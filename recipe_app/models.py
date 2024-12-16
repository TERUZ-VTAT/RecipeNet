from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


# Create your models here.

User = settings.AUTH_USER_MODEL


class PublicLevel(models.IntegerChoices):
    PRIVATE = 0, _("非公開")
    LIMITED_AND_PRIVATE = 1, _("限定公開")
    PUBLIC = 2, _("公開")


class Recipe(models.Model):
    title = models.CharField(
        verbose_name=_("title"),
        max_length=256,
    )
    user = models.ForeignKey(
        User,
        verbose_name=_("user"),
        on_delete=models.SET("DELETED_USER"),
    )  # TODO: on_deleteが動くか未検証
    recipe_code = models.CharField(
        verbose_name=_("recipe_code"),
        max_length=11,
        unique=True,
    )
    recipe_image = models.ImageField(
        verbose_name=_("recipe_image"),
        upload_to="recipe/thumbnails/",
        null=True
    )
    detail = models.TextField(
        verbose_name=_("detail"),
    )
    public_level = models.IntegerField(
        verbose_name=_("public_level"),
        choices=PublicLevel,
        default=0
    )
    favorite_count = models.BigIntegerField(
        verbose_name=_("favorite_count"),
        default=0
    )
    created_at = models.DateTimeField(
        verbose_name=_("created_at"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("updateded_at"),
        auto_now=True
    )


class RecipeSection(models.Model):
    index_num = models.IntegerField(
        verbose_name=_("index_num"),
    )
    detail = models.TextField(
        verbose_name=_("detail"),
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name=_("recipe"),
        on_delete=models.CASCADE,
    )


class IngredientsSection(models.Model):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=512,
    )
    amount = models.CharField(
        verbose_name=_("amount"),
        max_length=128
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name=_("recipe"),
        on_delete=models.CASCADE,
    )
    index_num = models.IntegerField(
        verbose_name=_("index_num"),
    )


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_("user"),
        on_delete=models.SET("DELETED_USER"),
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name=_("recipe"),
        on_delete=models.CASCADE
    )
