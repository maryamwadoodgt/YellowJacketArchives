from django.contrib import admin
from .models import UserLanguagePreference, CachedTranslation


@admin.register(UserLanguagePreference)
class UserLanguagePreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferred_language', 'updated_at')
    list_filter = ('preferred_language', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CachedTranslation)
class CachedTranslationAdmin(admin.ModelAdmin):
    list_display = ('source_language', 'target_language', 'source_text_preview', 'created_at')
    list_filter = ('source_language', 'target_language', 'created_at')
    search_fields = ('source_text', 'translated_text')
    readonly_fields = ('created_at',)

    def source_text_preview(self, obj):
        """Show preview of source text (first 50 chars)."""
        return obj.source_text[:50] + '...' if len(obj.source_text) > 50 else obj.source_text
    source_text_preview.short_description = 'Source Text'
