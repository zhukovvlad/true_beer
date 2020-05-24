from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Brewery

class BreweryCreateForm(forms.ModelForm):

    class Meta:
        model = Brewery
        fields = ['name', 'country', 'description', 'image']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }