from django.urls import path
from django.contrib.auth import views as auth_views

from .views import ThanksPage, CreateUserView

app_name = "users"

urlpatterns = [
    path("login/", CreateUserView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", CreateUserView.as_view(), name="signup"),
    path("thanks/", ThanksPage.as_view(), name="thanks"),
]
