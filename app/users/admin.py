from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ["last_name", "first_name"]
    list_display = [
        "first_name",
        "last_name",
        "username",
        "gender",
        "email",
        "uuid",
        "date_joined",
        "date_modified",
        "picture_updated",
        "is_active",
        "is_staff",
    ]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal Info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "gender",
                    "about",
                    "website",
                    "country",
                    "picture_updated",
                    "picture_file_path",
                    "picture",
                )
            },
        ),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
