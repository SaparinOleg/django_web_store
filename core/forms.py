from django.contrib.auth.forms import UserCreationForm
from django import forms

from core.models import User, Purchase, Refund


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'email': forms.EmailInput(),
            'password': forms.PasswordInput(),
        }


class PurchaseForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1)

    class Meta:
        model = Purchase
        fields = ['quantity']


class RefundForm(forms.ModelForm):
    class Meta:
        model = Refund
        fields = []
