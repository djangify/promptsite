from django.db import models


class Prompt(models.Model):
    CATEGORY_CHOICES = [
        ("marketing", "Marketing"),
        ("seo", "SEO"),
        ("social", "Social Media"),
        ("blog", "Blog & Content"),
        ("email", "Email Marketing"),
        ("sales", "Sales Pages"),
        ("local", "Local Business"),
        ("ads", "Advertising"),
        ("customer", "Customer Engagement"),
        ("video", "Video Scripts"),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField(help_text="The actual prompt text")
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default="marketing"
    )
    tags = models.CharField(
        max_length=255, blank=True, help_text="Comma-separated tags"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
