from django import forms
from django.contrib.auth import get_user_model

from .models import Beer, Vote

class BeerCreateForm(forms.ModelForm):
    hunter = forms.ModelChoiceField(
        widget=forms.HiddenInput(),
        queryset=get_user_model().objects.all(),
        disabled=True
    )

    class Meta:
        model = Beer
        fields = ['title', 'description', 'og', 'abv', 'ibu', 'hops', 'brewery', 'style', 'hunter']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'og': forms.NumberInput(attrs={'class': 'form-control'}),
            'abv': forms.NumberInput(attrs={'class': 'form-control'}),
            'ibu': forms.NumberInput(attrs={'class': 'form-control'}),
            'hops': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'brewery': forms.Select(attrs={'class': 'form-control'}),
            'style': forms.Select(attrs={'class': 'form-control'}),
        }

class VoteForm(forms.ModelForm):

    user = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=get_user_model().objects.all(),
        disabled=True,
    )

    beer = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=Beer.objects.all(),
        disabled=True,
    )

    value = forms.ChoiceField(
        label='Vote',
        widget=forms.RadioSelect,
        choices=Vote.VALUE_CHOICES,
    )

    class Meta:
        model = Vote
        fields = (
            'value', 'user', 'beer',
        )