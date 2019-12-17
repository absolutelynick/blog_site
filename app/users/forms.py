from django import forms
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput, validators=[validate_password]
    )

    class Meta:
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )
        model = get_user_model()
