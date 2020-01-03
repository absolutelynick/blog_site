from django.urls import path

from .views import (
    PostView,
    blog_post_list_view,
    blog_post_create_view,
    blog_post_update_view,
    blog_post_delete_view,
)

app_name = "blog"

urlpatterns = [
    path("posts/", blog_post_list_view, name="posts"),
    path("new-post/", blog_post_create_view, name="new"),
    path("post/<str:slug>/", PostView.as_view(), name="post"),
    path("edit/<str:slug>/", blog_post_update_view, name="edit"),
    path("delete/<str:slug>/", blog_post_delete_view, name="delete"),
]
