from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='First Name'
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='Last Name'
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'},),
        label='Email'
    )

    class Meta:
        model = User
        fields = ["first_name",
                  "last_name",
                  "username",
                  "email",
                  "password1",
                  "password2"
                  ]