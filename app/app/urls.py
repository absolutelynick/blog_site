"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


if not settings.DEBUG:
    # Two step auth

    from django_otp.admin import OTPAdminSite

    admin.site.__class__ = OTPAdminSite

urlpatterns = [
    # Admin
    path("supersite/admin2step/", admin.site.urls, name="admin"),
    # Site
    path("", include("core.urls")),
    path("users/", include("users.urls"), name="users"),
    path("blog/", include("blog.urls"), name="blog"),
    path("social-auth/", include("social_django.urls", namespace="social")),
]

# Adding local media handling

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Error Handlers # These will only work with debug as False

handler400 = "core.views.custom_400_page"
handler403 = "core.views.custom_403_page"
handler404 = "core.views.custom_404_page"
handler500 = "core.views.custom_500_page"
