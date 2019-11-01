from django.urls import path
from django.contrib.auth import views as auth_views

from .views import SignUp, ThanksPage

app_name = "users"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", SignUp.as_view(), name="signup"),
    path("thanks/", ThanksPage.as_view(), name="thanks"),
]
