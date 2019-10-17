from django.shortcuts import render


def home_page(request):
    return render(request, "index.html", {"title": "Index Page"})


def about_page(request):
    return render(request, "about.html", {"title": "About Page"})


def contact_page(request):
    return render(request, "contact.html", {"title": "Contact Page"})
