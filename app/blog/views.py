from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

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

    def get_post_comments(self, post):
        return Comment.objects.filter(post=post).order_by("-date_created")

    def get(self, request, *args, **kwargs):
        form = CommentForm(request.POST or None)
        post = get_object_or_404(BlogPost, slug=kwargs["slug"])
        comments = self.get_post_comments(post)
        context = {"post": post, "comments": comments, "form": form}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(BlogPost, slug=kwargs["slug"])

        if request.method == "POST":
            form = CommentForm(request.POST or None)

            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.comment = form.cleaned_data["comment"]
                comment.comment_by = request.user
                comment.save()

                form = CommentForm(None)

                messages.success(request, "Comment saved.")
            else:
                messages.error(request, "Error commenting.")

        comments = self.get_post_comments(post)
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


@login_required
@require_POST
def post_like_button(request):
    object_id = request.POST.get('id')
    action = request.POST.get('action')
    print(f"object_id: {object_id}")
    if object_id and action:
        try:
            post = BlogPost.objects.get(id=object_id)
            if action == 'like':
                post.liked_by.add(request.user)
            else:
                post.liked_by.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass

    return JsonResponse({'status':'ko'})