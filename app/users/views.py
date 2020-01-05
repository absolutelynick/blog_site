from django.shortcuts import render, get_object_or_404
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import UserCreateForm, UserEditForm
from .models import User
from blog.models import BlogPost
from api.utils.page_tools import get_pagination_page


class ProfileView(LoginRequiredMixin, TemplateView):
    """Profile Page"""

    template_name = "users/profile.html"

    def get(self, request, *args, **kwargs):
        # Get the user
        if kwargs.get("username", None):
            user = get_object_or_404(User, username=kwargs["username"])
        else:
            user = request.user

        # Get the users posts
        object_list = BlogPost.objects.filter(posted_by=user)
        page, posts = get_pagination_page(request, object_list)

        context = {
            "title": f"{user.full_name}",
            "posts": posts,
            "page": page,
            "user_profile": user,
        }
        return render(request, self.template_name, context=context)


class ProfileEditView(LoginRequiredMixin, TemplateView):
    """Profile Edit Page"""

    template = "users/profile_edit.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        # form = UserEditForm(request.POST)

        if request.method == "POST":
            form = UserEditForm(
                instance=request.user, data=request.POST, files=request.FILES
            )
            if form.is_valid():
                form.save()
        else:
            form = UserEditForm(instance=request.user)

            # Profile fields

            form.fields["first_name"].initial = request.user.first_name
            form.fields["first_name"].widget.attrs["autofocus"] = "autofocus"

            form.fields["last_name"].initial = request.user.last_name
            form.fields["email"].initial = request.user.email
            form.fields["username"].initial = request.user.username or None
            form.fields["gender"].initial = request.user.gender or None
            form.fields["date_of_birth"].initial = request.user.date_of_birth or None
            form.fields["about"].initial = request.user.about or None
            form.fields["website"].initial = request.user.website or None
            form.fields["country"].initial = request.user.country or None
            form.fields["picture"].initial = request.user.picture or None

        context = {"title": "Edit Profile", "form": form}
        return render(request, self.template, context=context)


@login_required
def save_edit(request):
    """Save the edited form"""
    if request.method == "POST":
        form = UserEditForm(
            instance=request.user, data=request.POST, files=request.FILES
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")

        else:
            messages.error(
                request,
                "Error updating your profile. Please fix the issues to save your changes.",
            )
    else:
        form = UserEditForm(instance=request.user)

    return render(
        request, "users/profile_edit.html", {"title": "Edit Profile", "form": form}
    )


class ThanksPage(TemplateView):
    """Thank you for signing up page"""

    template_name = "users/thank_you_for_signing_up.html"

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
    email_template_name = "users/password_reset_email.html"

    def get_context_data(self, **kwargs):
        context = super(PasswordResetView, self).get_context_data(**kwargs)
        context["title"] = "Reset Password"
        return context


class PasswordSendResetEmailView(TemplateView):
    """Resetting your password thank you"""

    template_name = "users/thank_you_for_resetting.html"

    def get(self, request, *args, **kwargs):
        context = {"title": "Thank you"}
        return render(request, self.template_name, context=context)


class PasswordChangeView(auth_views.PasswordChangeView):
    """Change user password"""

    template_name = "users/password_change_form.html"
    # success_url = reverse_lazy("users:profile", kwargs={'username': '{user.username}'})
    success_url = reverse_lazy("users:profile")

    def get_context_data(self, **kwargs):
        context = super(PasswordChangeView, self).get_context_data(**kwargs)
        context["title"] = "Change Password"
        return context


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """Confirm the change"""

    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    """Completed change password process that the password was changed"""

    template_name = "users/password_reset_complete.html"
