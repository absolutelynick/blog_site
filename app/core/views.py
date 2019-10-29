from django.shortcuts import render
from .forms import ContactForm


def home_page(request):
    return render(request, "index.html", {"title": "Index"})


def about_page(request):
    return render(request, "about.html", {"title": "About"})


def contact_page(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
    context = {"title": "Contact Us", "form": form}
    return render(request, "form.html", context)


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
