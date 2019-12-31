from django.contrib import admin
from django.utils.translation import gettext as _

from .models import BlogPost


@admin.register(BlogPost)
class BlogAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "slug",
        "content",
        "uuid",
        "hashtags",
        "posted_by",
        "date_created",
        "date_modified",
    ]
    fieldsets = (
        (_("Blog Info"), {"fields": ("title", "content")}),
        (
            _("Blog Creator Info"),
            {"fields": ("posted_by",)},
        ),
        (_("Base Info"), {"fields": ("liked_by", "uuid", "hashtags")}),
    )
    ordering = ["title", "date_created", "date_modified"]
    readonly_fields = ("uuid", "date_created")
