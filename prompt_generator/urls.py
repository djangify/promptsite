# prompt_generator/urls.py
from django.urls import path
from . import views

app_name = "prompt_generator"

urlpatterns = [
    path("", views.generator_list, name="generator_list"),
    path("<int:pk>/", views.generator_detail, name="generator_detail"),
    path(
        "save/<int:prompt_id>/", views.toggle_saved_prompt, name="toggle_saved_prompt"
    ),
]
