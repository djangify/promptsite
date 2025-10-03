from django.urls import path
from . import views

app_name = "prompt_templates"

urlpatterns = [
    path("<int:pk>/", views.prompt_fill_view, name="prompt_fill"),
]
