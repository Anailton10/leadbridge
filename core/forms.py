from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "w-full rounded-lg bg-gray-700 border-gray-600 focus:ring focus:ring-blue-500"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full rounded-lg bg-gray-700 border-gray-600 focus:ring focus:ring-blue-500"
            }
        )
    )
