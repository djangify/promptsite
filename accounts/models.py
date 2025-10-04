# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import uuid
from datetime import timedelta
from prompts.models import Prompt


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    verified = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True)

    # Business fields
    business_name = models.CharField(max_length=255, blank=True, null=True)
    business_type = models.CharField(max_length=255, blank=True, null=True)
    business_location = models.CharField(max_length=255, blank=True, null=True)
    target_audience = models.CharField(max_length=255, blank=True, null=True)

    # link to saved prompts
    saved_prompts = models.ManyToManyField(Prompt, blank=True, related_name="saved_by")
    # link to saved templates
    saved_templates = models.ManyToManyField(
        "prompt_templates.PromptTemplate", blank=True, related_name="saved_by"
    )

    def __str__(self):
        return f"{self.user.username}'s profile"


# Automatically create a UserProfile when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except User.profile.RelatedObjectDoesNotExist:
        UserProfile.objects.create(user=instance)


class EmailVerificationToken(models.Model):
    """Model for email verification tokens"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    reminder_sent = models.BooleanField(default=False)
    reminder_sent_at = models.DateTimeField(null=True, blank=True)

    def is_valid(self):
        # Token expires after 24 hours
        return self.created_at >= timezone.now() - timedelta(hours=24)

    def __str__(self):
        return f"Verification for {self.user.username}"
