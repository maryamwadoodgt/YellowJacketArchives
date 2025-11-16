from django.db import models
from django.contrib.auth.models import User


class UserLanguagePreference(models.Model):
    """Stores user's preferred language for the interface and content."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='language_preference')
    preferred_language = models.CharField(
        max_length=10,
        default='en',
        choices=[
            ('en', 'English'),
            ('es', 'Spanish'),
            ('fr', 'French'),
            ('de', 'German'),
            ('zh-hans', 'Simplified Chinese'),
            ('ja', 'Japanese'),
            ('pt', 'Portuguese'),
            ('hi', 'Hindi'),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.preferred_language}"


class CachedTranslation(models.Model):
    """Cache translations to avoid repeated API calls."""
    source_language = models.CharField(max_length=10)
    target_language = models.CharField(max_length=10)
    source_text = models.TextField()
    translated_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('source_language', 'target_language', 'source_text')
        indexes = [
            models.Index(fields=['source_language', 'target_language']),
        ]

    def __str__(self):
        return f"{self.source_language} -> {self.target_language}"
