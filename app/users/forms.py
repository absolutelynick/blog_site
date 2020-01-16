from django import forms
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import User
import datetime

YEAR = datetime.datetime.now().year + 1


class EmailSendForm(forms.Form):
    email = forms.EmailField()

    class Meta:
        fields = ("email",)


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput, validators=[validate_password]
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
        validators=[validate_password],
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


class DateInput(forms.DateInput):
    input_type = "date"


class UserEditForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField(required=True)

    email = forms.EmailField(required=True)

    date_of_birth = forms.DateField(label="Date of Birth", widget=DateInput())

    about = forms.CharField(
        max_length=255,
        widget=forms.Textarea(
            attrs={"placeholder": "About me...", "rows": "3", "required": True}
        ),
    )

    website = forms.URLField()

    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "email",
            "gender",
            "date_of_birth",
            "username",
            "about",
            "website",
            "country",
            "picture",
        )
