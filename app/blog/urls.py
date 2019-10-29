from django.urls import path

from .views import (
    blog_post_detail_veiw,
    blog_post_list_veiw,
    blog_post_create_veiw,
    blog_post_update_veiw,
    blog_post_delete_veiw,
)


urlpatterns = [
    path("", blog_post_list_veiw),
    path("new-post/", blog_post_create_veiw),
    # path("new-blog/", blog_post_create_veiw),
    path("<str:slug>/", blog_post_detail_veiw),
    path("<str:slug>/edit", blog_post_update_veiw),
    path("<str:slug>/delete", blog_post_delete_veiw),
]
