from django.urls import path

from .views import blog_post_detail_page


urlpatterns = [
    path("blog/<str:slug>/", blog_post_detail_page),
]
