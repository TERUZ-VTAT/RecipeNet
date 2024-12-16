from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseBadRequest, HttpResponseForbidden
from numerize.numerize import numerize
from django.urls import reverse
from urllib.parse import urlencode, urlparse
import string
import random
from .models import Recipe, RecipeSection, IngredientsSection, Favorites
from .forms import SettingForm

# Create your views here.


def __saveRecipe(request: HttpRequest, recipe_code=None):
    print(request.POST)
    # 料理名, 説明を取得
    title = request.POST["title"]
    detail = request.POST["detail"]
    # 料理名無しなら無題にする
    if title == "":
        title = "無題"
    # 材料情報を整形
    ingredints_names = request.POST.getlist("ingredients_name", [])
    ingredints_amounts = request.POST.getlist("ingredients_amount", [])
    ingredients = list(
        zip(
            range(1, len(ingredints_names)+1),  # 番号
            ingredints_names,  # 名称
            ingredints_amounts  # 数量
        )
    )
    # 手順に番号を割り振って整形
    section_details = request.POST.getlist("section_detail", [])
    sections = list(
        zip(
            range(1, len(section_details)+1),  # 番号
            section_details  # 内容
        )
    )
    # 整形したデータを元に保存
    print("==")
    print(detail)
    # レシピ本体の保存
    if recipe_code == None:  # ID未指定の場合の新規レシピ登録
        while True:
            recipe_code = ''.join(random.choice(
                string.ascii_letters+string.digits
            ) for _ in range(11))
            if not Recipe.objects.filter(recipe_code=recipe_code).exists():
                break
        Recipe(
            title=title,
            detail=detail,
            user=request.user,
            recipe_code=recipe_code
        ).save()
    else:  # ID指定済みの場合は情報を上書き
        # レシピ本体オブジェクトの取得
        recipe = get_object_or_404(Recipe, recipe_code=recipe_code)
        # 所有者の検証
        if recipe.user != request.user:
            HttpResponseForbidden("権限が不足しています。")
        # レシピ関連データの削除
        IngredientsSection.objects.filter(recipe=recipe).all().delete()
        RecipeSection.objects.filter(recipe=recipe).all().delete()
        # 情報の上書き
        recipe.title = title
        recipe.detail = detail
        recipe.user = request.user
        recipe_code = recipe_code
        recipe.save()
    # 材料の保存
    ingredients_bulk = [
        IngredientsSection(
            index_num=index_num,
            name=name,
            amount=amount,
            recipe=recipe,
        ) for index_num, name, amount in ingredients
    ]
    IngredientsSection.objects.bulk_create(ingredients_bulk)
    # 手順の保存
    sections_bulk = [
        RecipeSection(
            index_num=index_num,
            detail=detail,
            recipe=recipe
        ) for index_num, detail in sections
    ]
    RecipeSection.objects.bulk_create(sections_bulk)
    # レシピコードを戻す
    return recipe_code


def index(request):
    return render(request, "index.html")


@login_required
def create(request: HttpRequest):
    if request.method == "POST":
        recipe_code = __saveRecipe(request)
        url = reverse('recipeApp:edit')
        parameters = urlencode({"id": recipe_code})
        return redirect(f'{url}?{parameters}', permanent=False)
    return render(request, "recipe/create_edit.html")


@login_required
def edit(request: HttpRequest):
    recipe_code: str = request.GET.get("id", None)
    if request.method == "POST":
        __saveRecipe(request, recipe_code)
    recipe = get_object_or_404(Recipe, recipe_code=recipe_code)
    ingredients = list(IngredientsSection.objects.values_list(
        'name',
        'amount'
    ).filter(recipe=recipe))
    sections = list(RecipeSection.objects.values_list(
        'detail'
    ).filter(recipe=recipe))
    print(ingredients)
    print(sections)
    return render(request, "recipe/create_edit.html", {"title": recipe.title, "detail": recipe.detail, "ingredients": ingredients, "sections": sections})


@login_required
def myRecipe(request: HttpRequest):
    my_recipies = Recipe.objects.filter(user=request.user)
    return render(request, "recipe/my_recipe.html", {"recipies": my_recipies})


@login_required
def setting(request: HttpRequest):
    recipe_code: str = request.GET.get("id", None)
    recipe = get_object_or_404(Recipe, recipe_code=recipe_code)
    if request.method == 'POST':
        form = SettingForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return render(request, "recipe/settings.html", {"recipe": recipe, "form": form})
    form = SettingForm(instance=recipe)
    return render(request, "recipe/settings.html", {"recipe": recipe, "form": form})


def findRecipe(request: HttpRequest):
    top = Recipe.objects.order_by("-favorite_count")[:10]
    new = Recipe.objects.order_by("-created_at")[:10]
    my_favorite = []
    if not request.user.is_anonymous:
        my_favorite = [c[0] for c in Favorites.objects.values_list(
            'recipe'
        ).filter(user=request.user)]
    print(my_favorite)
    return render(request, "recipe/find_recipe.html", {"top": top, "new": new, "my_favorite": my_favorite})


def showRecipe(request: HttpRequest):
    recipe_code: str = request.GET.get("id", None)
    recipe = get_object_or_404(Recipe, recipe_code=recipe_code)
    recipeIngredients = IngredientsSection.objects.filter(recipe=recipe)
    recipeSections = RecipeSection.objects.filter(recipe=recipe)
    # 詳細情報用の変数群
    is_favorite = Favorites.objects.filter(
        user=request.user,
        recipe=recipe
    ).exists()
    favorite_count = numerize(recipe.favorite_count)
    return render(request, "recipe/show_recipe.html", {"recipe": recipe, "is_favorite": is_favorite, "favorite_count": favorite_count, "ingredients": recipeIngredients, "sections": recipeSections})


@login_required
def favoriteRecipe(request: HttpRequest):
    next_url = request.GET.get('next', '/')
    parsed_url = urlparse(next_url)
    if parsed_url.netloc and parsed_url.netloc != request.get_host():
        return HttpResponseBadRequest("不正なリダイレクト先が指定されました。")
    recipe_code: str = request.GET.get("id", None)
    if request.method == "POST":
        recipe = get_object_or_404(Recipe, recipe_code=recipe_code)
        try:
            Favorites.objects.get(
                user=request.user,
                recipe=recipe
            ).delete()
            recipe.favorite_count -= 1
            recipe.save()
        except Favorites.DoesNotExist:
            Favorites(
                user=request.user,
                recipe=recipe
            ).save()
            recipe.favorite_count += 1
            recipe.save()
    return redirect(next_url, permanent=False)
