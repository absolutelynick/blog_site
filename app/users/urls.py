from django.urls import path, include
from django.contrib.auth.views import LoginView as SignInView, LogoutView as SignOutView

from .views import (
    ThanksPage,
    CreateUserView,
    ProfileView,
    PasswordResetView,
    PasswordChangeView,
    PasswordSendResetEmailView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

app_name = "users"

urlpatterns = [
    path(
        "sign_in/",
        SignInView.as_view(template_name="users/sign_in.html"),
        name="sign_in",
    ),
    path(
        "sign_out/",
        SignOutView.as_view(template_name="core/home.html"),
        name="sign_out",
    ),
    path("sign_up/", CreateUserView.as_view(), name="sign_up"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("thank_you/", ThanksPage.as_view(), name="thank_you"),
    path(
        "reset_email_sent/",
        PasswordSendResetEmailView.as_view(),
        name="reset_email_sent",
    ),
    path("reset_password/", PasswordResetView.as_view(), name="reset_password"),
    path("change_password/", PasswordChangeView.as_view(), name="change_password"),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
