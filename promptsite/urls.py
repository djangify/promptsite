# promptsite/urls.py (project-level)
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render


def home(request):
    return render(request, "home.html")


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("prompts/", include("prompt_generator.urls")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("prompt_templates/", include("prompt_templates.urls")),
]
