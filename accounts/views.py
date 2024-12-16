from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from .forms import SignUpForm, SigninFrom, EditProfileForm
from .models import User
from recipe_app.models import Recipe, Favorites
from django.http import HttpResponse, HttpRequest

# Create your views here.


class SignupView(CreateView):
    """ ユーザー登録用ビュー """
    form_class = SignUpForm  # 作成した登録用フォームを設定
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("index")  # ユーザー作成後のリダイレクト先ページ

    def form_valid(self, form):
        # ユーザー作成後にそのままログイン状態にする設定
        response = super().form_valid(form)
        account_id = form.cleaned_data.get("account_id")
        password = form.cleaned_data.get("password1")
        user = authenticate(account_id=account_id, password=password)
        login(self.request, user)
        return response


class SigninView(BaseLoginView):
    form_class = SigninFrom
    template_name = "accounts/signin.html"


class LogoutView(BaseLogoutView):
    success_url = reverse_lazy("recipeApp:index")


# ==========<ここからテンプレ外>===========
def showProfile(request: HttpRequest):
    account_id: str = request.GET.get("id", None)
    user = get_object_or_404(User, account_id=account_id)
    user_recipies = Recipe.objects.filter(user=user)
    my_favorite = []
    if not request.user.is_anonymous:
        my_favorite = [c[0] for c in Favorites.objects.values_list(
            'recipe'
        ).filter(user=request.user)]
    return render(request, "accounts/profile.html", {"profile_user": user, "recipies": user_recipies, "my_favorite": my_favorite})


def editProfile(request: HttpRequest):
    form = EditProfileForm(instance=request.user)
    if request.method == "POST":
        form = EditProfileForm(
            request.POST,
            request.FILES,
            instance=request.user
        )
        print(form.is_valid())
        if form.is_valid():
            form.save()
    return render(request, "accounts/profile_edit.html", {"form": form})
