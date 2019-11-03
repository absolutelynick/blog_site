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

urlpatterns = [
    path("site/admin/", admin.site.urls),
    path("", include("core.urls")),
    path("users/", include("users.urls")),
    path("users/", include("django.contrib.auth.urls")),
    path("blog/", include("blog.urls")),
]

# Error Handlers # These will only work with debug as False

handler400 = "core.views.custom_400_page"
handler403 = "core.views.custom_403_page"
handler404 = "core.views.custom_404_page"
handler500 = "core.views.custom_500_page"