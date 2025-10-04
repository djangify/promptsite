from django.db import models
from django.utils.text import slugify


class PromptTemplate(models.Model):
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
    slug = models.SlugField(blank=True, null=True)
    template_text = models.TextField(
        help_text="Use placeholders like [business_name], [business_type], [business_location], [target_audience]"
    )
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default="marketing"
    )
    tips = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
