from django import forms
from .models import Recipe


class SettingForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['public_level']
