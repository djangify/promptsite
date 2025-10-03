from django.contrib import admin
from .models import PromptTemplate


@admin.register(PromptTemplate)
class PromptTemplateAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title", "template_text", "tips")
    list_filter = ("created_at",)
    fieldsets = (
        (None, {"fields": ("title", "template_text", "tips")}),
        (
            "Metadata",
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )
    readonly_fields = ("created_at",)
