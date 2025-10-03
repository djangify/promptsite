from django.db import models


class PromptTemplate(models.Model):
    title = models.CharField(max_length=255)
    template_text = models.TextField(
        help_text="Use placeholders like [business_name], [business_type], [business_location], [target_audience]"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
