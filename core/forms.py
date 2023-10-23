from django.contrib.auth.forms import UserCreationForm
from django import forms

from core.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'email': forms.EmailInput(),
            'password': forms.PasswordInput(),
        }
