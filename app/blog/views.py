from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse

from .models import BlogPost, Comment
from .forms import PostForm, CommentForm
from api.utils.page_tools import get_pagination_page


class BlogListView(LoginRequiredMixin, TemplateView):
    """Blog Post List Page"""

    template_name = "blog/posts.html"

    def get(self, request, *args, **kwargs):
        object_list = BlogPost.objects.all()
        page, posts = get_pagination_page(request, object_list)
        context = {"title": "Posts", "posts": posts, "page": page}
        return render(request, self.template_name, context=context)


class BlogPostCreateView(LoginRequiredMixin, TemplateView):
    """Blog Post Create Page"""

    template_name = "blog/create.html"

    def get(self, request, *args, **kwargs):
        form = form = PostForm()
        context = {"title": "Create Post", "form": form}
        return render(request, self.template_name, context=context)

    def post(self, request):
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                title = form.cleaned_data["title"]
                content = form.cleaned_data["content"]
                post.title = title
                post.content = content
                post.posted_by = request.user
                post.slug = title.replace(" ", "-")
                hastags = [i for i in content.split(" ") if "#" in i]
                post.hashtags = hastags
                post.save()

                messages.success(request, "Post saved.")

            else:
                messages.error(request, "Error posting.")
        else:
            form = PostForm()
        context = {"title": "Create Post", "form": form}
        return render(request, self.template_name, context=context)


class BlogPostView(LoginRequiredMixin, TemplateView):
    """Post view Page"""

    template_name = "blog/detail.html"

    def get(self, request, *args, **kwargs):
        form = CommentForm()
        post = get_object_or_404(BlogPost, slug=kwargs["slug"])
        comments = Comment.objects.filter(post=post).order_by("date_created")
        context = {"post": post, "comments": comments, "form": form}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(BlogPost, slug=kwargs["slug"])

        if request.method == "POST":
            form = CommentForm(request.POST)

            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.comment = form.cleaned_data["comment"]
                comment.save()

                messages.success(request, "Comment saved.")
            else:
                messages.error(request, "Error commenting.")

        comments = Comment.objects.filter(post=post).order_by("date_created")
        context = {"post": post, "comments": comments, "form": form}
        return render(request, self.template_name, context=context)

class BlogPostEditView(LoginRequiredMixin, TemplateView):
    """Post Edit View"""

    template_name = "blog/update.html"

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(BlogPost, slug=kwargs["slug"])
        context = {"object": obj}
        return render(request, self.template_name, context=context)


class BlogPostDeleteView(LoginRequiredMixin, TemplateView):
    """Post Delete View"""

    template_name = "blog/delete.html"

    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(BlogPost, slug=kwargs["slug"])
        context = {"object": obj}
        if obj:
            obj.delete()
        else:
            # Fail
            pass

        return render(request, self.template_name, context=context)


class CommentDeleteView(LoginRequiredMixin, TemplateView):
    """Delete a users comment on a post"""

    template_name = "blog/detail.html"

    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, uuid=kwargs["uuid"])
        post = comment.post

        comment.delete()

        return HttpResponseRedirect(reverse('blog:post', kwargs={'slug': post.slug}))
