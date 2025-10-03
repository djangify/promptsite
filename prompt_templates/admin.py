from django.contrib import admin
from .models import PromptTemplate


@admin.register(PromptTemplate)
class PromptTemplateAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title", "template_text")
    list_filter = ("created_at",)
