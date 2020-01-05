from django.urls import path

from .views import (
    BlogPostView,
    BlogListView,
    BlogPostCreateView,
    BlogPostEditView,
    BlogPostDeleteView,
)

app_name = "blog"

urlpatterns = [
    path("posts/", BlogListView.as_view(), name="posts"),
    path("new/", BlogPostCreateView.as_view(), name="new"),
    path("post/<str:slug>/", BlogPostView.as_view(), name="post"),
    path("edit/<str:slug>/", BlogPostEditView.as_view(), name="edit"),
    path("delete/<str:slug>/", BlogPostDeleteView.as_view(), name="delete"),
]
