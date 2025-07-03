from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *


class GenreForms(forms.ModelForm):
    class Meta:
        model = Genres
        fields = '__all__'

        labels = {
            'name': "Janr nomi",
            'slug': "Slug (URL uchun ixtiyoriy)"
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "Masalan: Drama",
            }),
            'slug': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "Masalan: drama",
            })
        }

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if Genres.objects.filter(slug=slug).exists():
            raise ValidationError(f"\"{slug}\" URL allaqachon qo'shilgan.")
        return slug

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].required = True
        self.fields['slug'].required = False


class MovieForms(forms.ModelForm):
    class Meta:
        model = Movies
        fields = '__all__'

        labels = {
            'name': "Film nomi",
            'slug': "Slug (URL uchun ixtiyoriy)",
            'genre': "Film janri",
            'photo': "Film surati",
            'video': "Film videosi",
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "Masalan: Jinoyatchilar shahri"
            }),
            'slug': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "Masalan: jinoyatchilar-shahri"
            }),
            'genre': forms.CheckboxSelectMultiple(),
            'country': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "Masalan: Janubiy Korea"
            }),
            'year': forms.NumberInput(attrs={
                'class': "form-control",
                'min': 1900
            }),
            'language': forms.Select(attrs={
                'class': "form-select",
            }),
            'duration': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "Masalan: 1 soat 40 daqiqa"
            }),
            'age': forms.Select(attrs={
                'class': "form-select"
            }),
            'photo': forms.FileInput(attrs={
                'class': "form-control",
                'accept': "image/*"
            }),
            'video': forms.FileInput(attrs={
                'class': "form-control",
                'accept': "video/*"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['slug'].required = False

        old_choices = list(self.fields['language'].choices)
        filtered_choices = [choice for choice in old_choices if choice[0] != '']
        self.fields['language'].choices = [('', 'Tanlang')] + filtered_choices

        old_choices = list(self.fields['age'].choices)
        filtered_choices = [choice for choice in old_choices if choice[0] != '']
        self.fields['age'].choices = [('', 'Tanlang')] + filtered_choices

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if Genres.objects.filter(slug=slug).exists():
            raise ValidationError(f"\"{slug}\" URL allaqachon qo'shilgan.")
        return slug


class LoginForms(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        username = self.fields['username']
        password = self.fields['password']

        username.label = "Foydalanuvchi nomi"
        password.label = "Parol"

        username.widget.attrs.update({
            'class': "form-control",
        })
        password.widget.attrs.update({
            'class': "form-control",
        })
