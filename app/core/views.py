from django.shortcuts import render
from django.conf import settings
from django.urls import reverse_lazy

from .forms import Contact_Form


def home_page(request):
    return render(request, "core/home.html", {"title": "Home"})


def about_page(request):
    return render(request, "core/about.html", {"title": "About"})


def contact_page(request):
    form = Contact_Form(request.POST or None)

    if form.is_valid():
        if settings.DEBUG:
            print(form.cleaned_data)

        name = f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']}"

        context = dict(
            title="Thank you",
            header=f"Thank you for contacting us {name}!",
            body="We will get back you as soon as we can. ",
            url_text="Click below to head to the login page.",
            url=reverse_lazy("users:sign_in"),
            url_button_text="Sign in",
        )

        return render(request, "response.html", context)

    if request.user.is_authenticated:
        form.fields["first_name"].initial = request.user.first_name
        form.fields["first_name"].widget.attrs["readonly"] = True
        form.fields["last_name"].initial = request.user.last_name
        form.fields["last_name"].widget.attrs["readonly"] = True
        form.fields["email"].initial = request.user.email
        form.fields["email"].widget.attrs["readonly"] = True
        form.fields["content"].widget.attrs[
            "placeholder"
        ] = f"Hi {request.user.first_name}, let us know what you are thinking"
        form.fields["content"].widget.attrs["autofocus"] = "autofocus"
    else:
        form.fields["first_name"].widget.attrs["autofocus"] = "autofocus"

    context = {"title": "Contact Us", "form": form}
    return render(request, "core/form.html", context)


def custom_400_page(request, exc):
    context = {
        "error_title": "400 Error",
        "error_text": "The page was not found",
        "exception": str(exc),
    }
    return render(request, "error.html", context)


def custom_403_page(request, exc):
    context = {
        "error_title": "403 Error",
        "error_text": "This page is forbidden",
        "exception": str(exc),
    }
    return render(request, "error.html", context)


def custom_404_page(request, exc):
    context = {
        "error_title": "404 Error",
        "error_text": "The page was not found",
        "exception": str(exc),
    }
    return render(request, "error.html", context)


def custom_500_page(request):
    context = {
        "error_title": "500 Error",
        "error_text": "There has been an internal server error",
        "exception": None,
    }
    return render(request, "error.html", context)


def error_page(request):
    return custom_404_page(request, "404")
