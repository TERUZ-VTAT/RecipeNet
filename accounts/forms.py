from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
import mimetypes

from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "account_id",
            "email",
            "birth_date",
        )


class SigninFrom(AuthenticationForm):
    class Meta:
        model = User


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "account_id",
            "account_name",
            "avatar",
        )

    def clean_avatar(self):
        print("called")
        uploaded_file = self.cleaned_data['avatar']
        mime_type, encoding = mimetypes.guess_type(uploaded_file.name)
        if mime_type not in ['image/svg+xml', 'image/webp', 'image/png', 'image/jpeg', 'image/gif']:
            raise ValidationError('サポートされていないファイル形式です。')
        return uploaded_file
