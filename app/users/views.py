from django.shortcuts import render, get_object_or_404
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core import signing

from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from rest_framework.response import Response
from rest_framework import status

from .forms import UserCreateForm, UserEditForm, EmailSendForm
from .models import User
from blog.models import BlogPost
from api.utils.page_tools import get_pagination_page
from api.message.tasks import send_confirm_email_link

import datetime


class ProfileView(LoginRequiredMixin, TemplateView):
    """Profile Page"""

    template_name = "users/profile.html"

    def get(self, request, *args, **kwargs):
        # Get the user
        if kwargs.get("slug", None):
            user = get_object_or_404(User, slug=kwargs["slug"])
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


class ThanksForSigningUpPage(TemplateView):
    """Thank you for signing up page"""

    template_name = "response.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context=self.get_context_data())

    def get_context_data(self):
        context = dict(
            title = "Thank you",
            header = "Thank you for signing up!",
            body = "Your user details will be deleted after two days if "
                   "you do not follow the link in your email.",
            url_text = "Click below to head to the login page.",
            url = reverse_lazy("users:sign_in"),
            url_button_text = "Sign in",
        )
        return context

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

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            send_confirm_email_link(form.cleaned_data["email"])

            return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name, {'form': form})


class EmailConfirmationView(TemplateView):
    template_name = "response.html"

    def get_context_data(self):
        context = dict(
            title = "Email Confirmation",
            header = "Email Verified",
            body = "Please feel free to sign in and use your account",
            url_text = "Please click below",
            url = reverse_lazy("users:sign_in"),
            url_button_text = "Sign in",
        )
        return context

    def get(self, request, *args, **kwargs):
        token = request.GET.get("token", False)

        if token:
            success = self.confirm_user_email(token)
            context = self.get_context_data()

            if not success:
                 context["title"] = "Email NOT Confirmed"
                 context["header"] = "Email NOT Verified"
                 context["body"] = "Your email not found. Please try again."
                 context["url_text"] = "Please enter your details on the sign in page"
                 context["url"] = reverse_lazy("users:resend_verification")
                 context["url_button_text"] = "Resend confirmation"

            return render(request, self.template_name, self.get_context_data())

        return Response(status=status.HTTP_404_NOT_FOUND)

    def confirm_user_email(self, token):
        try:
            data = signing.loads(token, max_age=datetime.timedelta(days=3))
        except signing.BadSignature:
            return False

        user = get_object_or_404(User, uuid=data["user_uuid"])
        user.is_active = True
        user.save()

        return True


class ResendEmailConfirmationView(TemplateView):
    template_name = "users/email_to_reset_form.html"
    success_url = "response.html"
    form_class = EmailSendForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        context = self.get_context_data()

        if form.is_valid():

            email = form.cleaned_data["email"]

            if User.objects.filter(email=email).exists():

                send_confirm_email_link(email)

                context["header"] = "Email Confirmation Sent"
                context["body"] = "You should receive an email with a link to " \
                                  "confirm you address."
                context["url_text"] = "Follow the link to sign in that you receive"
                context["url"] = reverse_lazy("users:sign_in")
                context["url_button_text"] = "Sign in"
                del context["form"]

            else:

                context["header"]= "Please sign up"
                context["body"]= f"Email '{email}' not found please go to the sign up page"
                context["url_text"]= "Please enter your details on the sign in page"
                context["url"]= reverse_lazy("users:sign_up")
                context["url_button_text"]= "Sign up"

            return render(request, self.success_url, context)

        return render(request, self.template_name, context)

    def get_context_data(self):
        context = dict(
            title = "Email Confirmation",
            header = "Email Confirmation",
            body = "Please enter your email below",
            url_text = "Please then follow the link in your email to confirm your email so we can send you a link",
            url = "users:resend_verification",
            url_button_text = "Resend Verification",
            form = "self.form_class"
        )
        return context


class PasswordResetEmailSendView(auth_views.PasswordResetView):
    """Reset user password email"""

    template_name = "users/email_to_reset_form.html"
    success_url = reverse_lazy("users:reset_email_sent")
    email_template_name = "users/password_reset_email.html"

    def get_context_data(self, **kwargs):
        context = super(PasswordResetEmailSendView, self).get_context_data(**kwargs)
        context["title"] = "Reset Password"
        return context


class PasswordSendResetEmailSetView(TemplateView):
    """Resetting your password thank you"""
    template_name = "response.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context=self.get_context_data())

    def get_context_data(self):
        context = dict(
            title = "Thank you",
            header = "Thank you for resetting!",
            body = "If you don't receive an email, please make sure you've "
                   "entered the email you registered with.",
            url_text = "Click below to head to the login page.",
            url = reverse_lazy("users:sign_in"),
            url_button_text = "Sign in",
        )
        return context

class PasswordChangeView(auth_views.PasswordChangeView):
    """Change user password"""

    template_name = "users/password_change_form.html"

    def get_context_data(self, **kwargs):
        context = super(PasswordChangeView, self).get_context_data(**kwargs)
        context["title"] = "Change Password"
        return context

    def get_success_url(self):
        user = self.get_form_kwargs()["user"]
        return reverse_lazy("users:profile", kwargs={"slug": user.slug})


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """Confirm the change"""

    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    """Completed change password process that the password was changed"""

    template_name = "users/password_reset_complete.html"

    def get(self, request, *args, **kwargs):

        print(f"success user request: {request}")
        print(f"success user request: {request.user}")
        print(f"success user args: {args}")
        print(f"success user kwargs: {kwargs}")

        return render(request, self.template_name, context=self.get_context_data())
