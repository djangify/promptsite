from django.urls import path
from . import views

app_name = "prompt_templates"

urlpatterns = [
    path("", views.template_list_view, name="template_list"),
    path("<slug:slug>/", views.prompt_fill_view, name="prompt_fill"),
    path("save/<slug:slug>/", views.save_template, name="save_template"),
    path(
        "dashboard/templates/",
        views.dashboard_saved_templates,
        name="dashboard_saved_templates",
    ),
]
