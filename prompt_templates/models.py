from django.db import models
from django.utils.text import slugify


class PromptTemplate(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    template_text = models.TextField(
        help_text="Use placeholders like [business_name], [business_type], [business_location], [target_audience]"
    )
    tips = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
