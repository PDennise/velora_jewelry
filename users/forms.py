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
    phone = forms.CharField(
        max_length=20,
        required=True,
        label='Phone Number'
    )
    class Meta:
        model = User
        fields = ["first_name",
                  "last_name",
                  "username",
                  "email",
                  "phone",
                  "password1",
                  "password2"
        ]

    def save(self, commit=True):
        user = super().save(commit)

        user.profile.default_phone_number = self.cleaned_data['phone']
        user.profile.save()

        return user