from django.shortcuts import render
from .forms import Contact_Form


def home_page(request):
    return render(request, "core/home.html", {"title": "Home"})


def about_page(request):
    return render(request, "core/about.html", {"title": "About"})


def contact_page(request):
    form = Contact_Form(request.POST or None)

    if form.is_valid():
        print(form.cleaned_data)
        context = {
            "title": "Contact Us",
            "first_name": form.cleaned_data["first_name"],
            "last_name": form.cleaned_data["last_name"],
        }
        return render(request, "core/thank_you_for_signing_up.html", context)

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
        "error_title": "500 Error",
        "error_text": "Sorry but there has been a server error",
        "exception": str(exc),
    }
    return render(request, "error.html", context)


def custom_403_page(request, exc):
    context = {
        "error_title": "500 Error",
        "error_text": "Sorry but there has been a server error",
        "exception": str(exc),
    }
    return render(request, "error.html", context)


def custom_404_page(request, exc):
    context = {
        "error_title": "500 Error",
        "error_text": "Sorry but there has been a server error",
        "exception": str(exc),
    }
    return render(request, "error.html", context)


def custom_500_page(request):
    context = {
        "error_title": "500 Error",
        "error_text": "Sorry but there has been a server error",
        "exception": None,
    }
    return render(request, "error.html", context)
