from django.urls import path

from .views import (
    BlogPostView,
    BlogListView,
    BlogPostCreateView,
    BlogPostEditView,
    BlogPostDeleteView,
    CommentDeleteView,
    post_like_button,
)

app_name = "blog"

urlpatterns = [
    path("posts/", BlogListView.as_view(), name="posts"),
    path("new/", BlogPostCreateView.as_view(), name="new"),
    path("post/<str:slug>/", BlogPostView.as_view(), name="post"),
    path('like/', post_like_button, name='like'),
    path("edit/<str:slug>/", BlogPostEditView.as_view(), name="edit"),
    path("delete/<str:slug>/", BlogPostDeleteView.as_view(), name="delete"),
    path("comment_delete/<str:uuid>/", CommentDeleteView.as_view(), name="comment_delete"),
]
