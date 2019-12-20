from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserCreateForm


class ProfileView(LoginRequiredMixin, TemplateView):
    """Profile Page"""

    template_name = "users/profile.html"

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.has_picture:
            profile_pic = user.profile_picture_path
        else:
            placeholder = static("images/users/placeholder.png")
            profile_pic = placeholder

        context = {"title": f"{user.full_name} {user}", "image": profile_pic}
        return render(request, self.template_name, context=context)


class ThanksPage(TemplateView):
    """Thank you for signing up page"""

    template_name = "users/thank_you.html"

    def get(self, request, *args, **kwargs):
        context = {"title": "Thank you"}
        return render(request, self.template_name, context=context)


class CreateUserView(CreateView):
    """Create a new user with custom template"""

    form_class = UserCreateForm
    success_url = reverse_lazy("users:thank_you")
    template_name = "users/sign_up_form.html"
    context = {"title": "Sign Up"}

    def get_context_data(self, **kwargs):
        context = super(CreateUserView, self).get_context_data(**kwargs)
        context["title"] = "Sign Up"
        return context


class PasswordResetView(auth_views.PasswordResetView):
    """Reset user password email"""

    template_name = "users/password_reset_form.html"
    success_url = reverse_lazy("users:reset_email_sent")

    def get_context_data(self, **kwargs):
        context = super(PasswordResetView, self).get_context_data(**kwargs)
        context["title"] = "Reset Password"
        return context


class PasswordResetEmailSentView(TemplateView):
    """Thank you reseting your password"""

    template_name = "users/thank_you_for_resetting.html"

    def get(self, request, *args, **kwargs):
        context = {"title": "Thank you"}
        return render(request, self.template_name, context=context)


class PasswordChangeView(auth_views.PasswordChangeView):
    """Change user password"""

    template_name = "users/password_change_form.html"
    success_url = reverse_lazy("users:profile")

    def get_context_data(self, **kwargs):
        context = super(PasswordChangeView, self).get_context_data(**kwargs)
        context["title"] = "Change Password"
        return context
