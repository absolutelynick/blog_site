from django.shortcuts import render
from django import forms
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic import CreateView

# from django.http import HttpResponseRedirect
# from django.contrib.auth.mixins import LoginRequiredMixin
#
# from .models import User
from .forms import UserCreateForm


class ThanksPage(TemplateView):
    """Thank you for signing up page"""

    template_name = "users/thankyou.html"

    def get(self, request, *args, **kwargs):
        context = {"title": "Thank you"}
        return render(request, self.template_name, context=context)


class CreateUserView(CreateView):
    """Create a new user with custom template"""

    form_class = UserCreateForm
    success_url = reverse_lazy("users:thanks")
    template_name = "users/user_form.html"

    # model = User
    # success_url = reverse_lazy("users:thanks")

    # model = User
    # form_class = Sign_Up_Form
    # success_url = reverse_lazy("users:thanks")
    # template_name = "users/user_form.html"
    # context = {"title": "Sign up", "form": form}
    # fields = ["first_name", "last_name", "username", "email", "password"]

    # def get(self, request, *args, **kwargs):
    #     form = Sign_Up_Form(request.POST or None)
    #     context = {"title": "Sign up", "form": form}
    #     return render(request, self.template_name, context=context)

    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class)
    #     form.fields['password'].widget = forms.PasswordInput()
    #     return form

    #
    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     self.object = form.save()
    #     return super().form_valid(form)
