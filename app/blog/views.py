from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import BlogPost
from .forms import BlogPostForm, BlogPostModelForm


def blog_post_list_veiw(request):
    # This could be a list or search view
    qs = BlogPost.objects.all()
    template_name = "blog/list.html"
    context = {"object_list": qs}
    return render(request, template_name, context)


def blog_post_create_veiw(request):
    # Create objects or use a form
    form = BlogPostModelForm(request.POST or None)
    if form.is_valid():
        if settings.DEBUG:
            print(form.cleaned_data)
        form.save()
        form = BlogPostModelForm()

    template_name = "blog/create.html"
    context = {"form": form, "title": "Create Post"}
    return render(request, template_name, context)


def blog_post_detail_veiw(request, slug):
    # An object --> detail view
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = "blog/detail.html"
    context = {"object": obj}
    return render(request, template_name, context)


def blog_post_update_veiw(request, slug):
    # Append or update the data that we are working with
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = "blog/update.html"
    context = {"object": obj, "form": None}
    return render(request, template_name, context)


def blog_post_delete_veiw(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = "blog/delete.html"
    context = {"object": obj}
    return render(request, template_name, context)
