from django.contrib import admin
from .models import PromptTemplate


@admin.register(PromptTemplate)
class PromptTemplateAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at")
    list_editable = ("category",)
    search_fields = ("title", "template_text", "tips")
    list_filter = ("category", "created_at")
    ordering = ("-created_at",)
    fieldsets = (
        (None, {"fields": ("title", "category", "template_text", "tips")}),
        (
            "Metadata",
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )
    readonly_fields = ("created_at",)
