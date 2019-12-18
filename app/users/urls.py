from django.urls import path
from django.contrib.auth import views as auth_views

from .views import ThanksPage, CreateUserView, ProfileView

app_name = "users"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="core/home.html"),
        name="logout",
    ),
    path("signup/", CreateUserView.as_view(), name="signup"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("thanks/", ThanksPage.as_view(), name="thanks"),
]
