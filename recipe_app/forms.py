from django import forms
from .models import Recipe
from django.core.exceptions import ValidationError
import mimetypes


class SettingForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['public_level']


class ThumbnailForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('recipe_image',)

    def clean_recipe_image(self):
        uploaded_file = self.cleaned_data['recipe_image']
        mime_type, encoding = mimetypes.guess_type(uploaded_file.name)
        if mime_type not in ['image/svg+xml', 'image/webp', 'image/png', 'image/jpeg', 'image/gif']:
            raise ValidationError('サポートされていないファイル形式です。')
        return uploaded_file
