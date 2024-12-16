from django.urls import path, include
from . import views

app_name = "recipeApp"

urlpatterns = [
    path('new', views.create, name='create'),
    # ↓example: `/recipe/edit?id=9KqIEb6qQOk`
    path('edit', views.edit, name='edit'),
    path('setting', views.setting, name="setting"),
    path('my-recipe', views.myRecipe, name='my-recipe'),
    path('find', views.findRecipe, name='find'),
    path('show', views.showRecipe, name='show'),
    path('favorite', views.favoriteRecipe, name='favorite')
]
