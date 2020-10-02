from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Beer, Vote, BeerComment

class BeerCreateForm(forms.ModelForm):
    hunter = forms.ModelChoiceField(
        widget=forms.HiddenInput(),
        queryset=get_user_model().objects.all(),
        disabled=True
    )

    class Meta:
        model = Beer
        fields = ['title', 'version', 'description', 'image', 'og', 'abv', 'ibu', 'hops', 'brewery', 'style', 'hunter']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'version': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sometimes some beer has different versions. Here you can enter this version.'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            #'image': forms.ImageField(attrs={'class': 'form-control'}),
            'og': forms.NumberInput(attrs={'class': 'form-control'}),
            'abv': forms.NumberInput(attrs={'class': 'form-control'}),
            'ibu': forms.NumberInput(attrs={'class': 'form-control'}),
            'hops': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'brewery': forms.Select(attrs={'class': 'form-control'}),
            'style': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        new_title = self.cleaned_data.get('title')
        if new_title == 'fuck':
            raise ValidationError('Shut up your mouth')
        #if set(x.id for x in Beer.objects.filter(title__iexact=new_title.lower())):
        #    raise ValidationError(f"Sorry, but \'{new_title}\' beer already exists.")
        return new_title
    
    def clean(self):
        cleaned_data = super(BeerCreateForm, self).clean()
        clean_title = cleaned_data.get('title')
        clean_version = cleaned_data.get('version')
        clean_brewery = cleaned_data.get('brewery')
        if not clean_title:
            raise forms.ValidationError('Your data is not clean')
        print('TITLE is', clean_title)
        print('VERSION is', clean_version)
        print('BREWERY is', clean_brewery)

        qs = Beer.objects.filter(brewery__name=clean_brewery)
        print('QS Brewery is ', qs)
        qs = qs.filter(title__iexact=clean_title.lower())
        if clean_version:
            qs = qs.filter(version__isnull=False, version__iexact=clean_version)
        print('QS is ', qs, qs.count())
        print('Cleaned_data is ', cleaned_data)
        if qs:
            raise forms.ValidationError(f"We can not help you. We already have \'{clean_title}\' beer brewed by \'{clean_brewery}\' in this version.")
        return cleaned_data


class BeerUpdateForm(forms.ModelForm):
    hunter = forms.ModelChoiceField(
        widget=forms.HiddenInput(),
        queryset=get_user_model().objects.all(),
        disabled=True
    )

    class Meta:
        model = Beer
        fields = ['title', 'version', 'description', 'image', 'og', 'abv', 'ibu', 'hops', 'brewery', 'style', 'hunter']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'version': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sometimes some beer has different versions. Here you can enter this version.'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            #'image': forms.ImageField(attrs={'class': 'form-control'}),
            'og': forms.NumberInput(attrs={'class': 'form-control'}),
            'abv': forms.NumberInput(attrs={'class': 'form-control'}),
            'ibu': forms.NumberInput(attrs={'class': 'form-control'}),
            'hops': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'brewery': forms.Select(attrs={'class': 'form-control'}),
            'style': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        new_title = self.cleaned_data.get('title')
        if new_title == 'fuck':
            raise ValidationError('Shut up your mouth')
        #if set(x.id for x in Beer.objects.filter(title__iexact=new_title.lower())):
        #    raise ValidationError(f"Sorry, but \'{new_title}\' beer already exists.")
        return new_title
    
    def clean(self):
        cleaned_data = super(BeerUpdateForm, self).clean()
        print(cleaned_data)
        clean_title = cleaned_data.get('title')
        clean_version = cleaned_data.get('version')
        clean_brewery = cleaned_data.get('brewery')
        if not clean_title:
            raise forms.ValidationError('Your data is not clean')
        print('TITLE is', clean_title)
        print('VERSION is', clean_version)
        print('BREWERY is', clean_brewery)

        #qs = Beer.objects.filter(brewery__name=clean_brewery)
        #print('QS Brewery is ', qs)
        #qs = qs.filter(title__iexact=clean_title.lower())
        #if clean_version:
        #    qs = qs.filter(version__isnull=False, version__iexact=clean_version)
        #print('QS is ', qs, qs.count())
        #print('Cleaned_data is ', cleaned_data)
        #if qs.count() > 0 and qs[0].id:
        #    raise forms.ValidationError(f"We can not help you. We already have \'{clean_title}\' beer brewed by \'{clean_brewery}\' in this version.")
        return cleaned_data


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
        widget=forms.RadioSelect(attrs={'class': 'custom-input'}),
        choices=Vote.VALUE_CHOICES,
    )

    class Meta:
        model = Vote
        fields = (
            'value', 'user', 'beer',
        )


class BeerCommentForm(forms.ModelForm):

    '''author = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=get_user_model().objects.all(),
        disabled=True,
    )

    beer = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=Beer.objects.all(),
        disabled=True,
    )'''
    
    class Meta:
        model = BeerComment
        fields = ('title', 'body', 'author', 'beer',)
        widgets = {
            'author': forms.HiddenInput(),
            'beer': forms.HiddenInput(),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.TextInput(attrs={'class': 'form-control'})
                    }

