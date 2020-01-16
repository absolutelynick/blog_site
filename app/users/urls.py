from django.urls import path
from django.contrib.auth.views import LoginView as SignInView, LogoutView as SignOutView

from .views import (
    ThanksForSigningUpPage,
    CreateUserView,
    ProfileView,
    ProfileEditView,
    PasswordChangeView,
    PasswordSendResetEmailSetView,
    PasswordResetEmailSendView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    EmailConfirmationView,
    ResendEmailConfirmationView,
    save_edit,
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
    path(
        "confirm_user_email/",
        EmailConfirmationView.as_view(),
        name="confirm_user_email",
    ),
    path(
        "resend_confirm_user_email/",
        ResendEmailConfirmationView.as_view(),
        name="resend_verification",
    ),
    path("sign_up/", CreateUserView.as_view(), name="sign_up"),
    path("profile/<str:slug>/", ProfileView.as_view(), name="profile"),
    path("profile_edit/", ProfileEditView.as_view(), name="profile_edit"),
    path("profile_save/", save_edit, name="save_edit"),
    path("thank_you/", ThanksForSigningUpPage.as_view(), name="thank_you"),
    path(
        "reset_email_sent/",
        PasswordSendResetEmailSetView.as_view(),
        name="reset_email_sent",
    ),
    path(
        "reset_password/", PasswordResetEmailSendView.as_view(), name="reset_password"
    ),
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
