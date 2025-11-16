# Multi-Language Translation Setup Guide

This document explains how the translation feature works in Yellow Jacket Archives and how to use it.

## Overview

The GT Library Store now supports **8 languages** with automatic translation capabilities:
- 🇺🇸 English
- 🇪🇸 Spanish  
- 🇫🇷 French
- 🇩🇪 German
- 🇨🇳 Simplified Chinese
- 🇯🇵 Japanese
- 🇵🇹 Portuguese
- 🇮🇳 Hindi

## Architecture

### Technology Stack

1. **Django i18n Framework**
   - Built-in internationalization support
   - Automatic language detection via `LocaleMiddleware`
   - URL-based language prefixing (e.g., `/es/movies/`, `/fr/movies/`)

2. **LibreTranslate API**
   - Free, open-source translation service (no API key required)
   - Public endpoint: `https://libretranslate.com/translate`
   - Provides real-time translation of content

3. **Caching System**
   - `CachedTranslation` model stores translated text
   - Reduces redundant API calls
   - Improves performance for frequently translated content

4. **User Preferences**
   - `UserLanguagePreference` model stores each user's language choice
   - OneToOne relationship with Django User model
   - Persistent across sessions

## Database Models

### UserLanguagePreference

```python
class UserLanguagePreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_language = models.CharField(max_length=10, default='en')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

Stores each authenticated user's preferred language.

### CachedTranslation

```python
class CachedTranslation(models.Model):
    source_language = models.CharField(max_length=10)
    target_language = models.CharField(max_length=10)
    source_text = models.TextField()
    translated_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('source_language', 'target_language', 'source_text')
```

Caches translation results to minimize API calls and improve performance.

## API Endpoints

All endpoints use language-prefixed URLs (e.g., `/en/`, `/es/`, `/fr/`, etc.).

### 1. Translate Text

**Endpoint:** `POST /translations/translate/`

**Request:**
```json
{
    "text": "Hello World",
    "source_language": "en",
    "target_language": "es"
}
```

**Response (Success):**
```json
{
    "success": true,
    "original": "Hello World",
    "translated": "Hola Mundo",
    "source_language": "en",
    "target_language": "es",
    "cached": false
}
```

**Response (Error):**
```json
{
    "success": false,
    "error": "No text provided"
}
```

**Features:**
- Public endpoint (no authentication required)
- Caches results automatically
- Returns `"cached": true` if result was retrieved from cache
- Returns original text if source and target languages are the same

---

### 2. Set User Language Preference

**Endpoint:** `POST /translations/set-preference/`

**Authentication:** Required (login required)

**Request:**
```json
{
    "language": "es"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Language preference updated",
    "language": "es"
}
```

**Valid Languages:**
- `en` - English
- `es` - Spanish
- `fr` - French
- `de` - German
- `zh-hans` - Simplified Chinese
- `ja` - Japanese
- `pt` - Portuguese
- `hi` - Hindi

---

### 3. Get User Language Preference

**Endpoint:** `GET /translations/get-preference/`

**Authentication:** Required (login required)

**Response:**
```json
{
    "success": true,
    "language": "es"
}
```

**Default:** Returns "en" (English) if no preference is set.

## Language Selector UI

The navbar includes a language dropdown menu with flags:

```html
<!-- Language Selector in base.html -->
<div class="nav-item dropdown me-3">
  <a class="nav-link dropdown-toggle" href="#" id="languageDropdown">
    <i class="fas fa-globe me-1"></i> Language
  </a>
  <ul class="dropdown-menu dropdown-menu-end">
    <li><a class="dropdown-item" href="{% url 'django.views.i18n.set_language' %}?language=en">
      🇺🇸 English
    </a></li>
    <li><a class="dropdown-item" href="{% url 'django.views.i18n.set_language' %}?language=es">
      🇪🇸 Español
    </a></li>
    <!-- ... more languages ... -->
  </ul>
</div>
```

**How It Works:**
1. User clicks a language in the dropdown
2. Django's `set_language` view sets the language cookie
3. `LocaleMiddleware` detects the cookie and adjusts the language
4. URLs are automatically prefixed with language code (e.g., `/es/movies/`)

## Configuration Files

### settings.py

```python
LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('en', 'English'),
    ('es', 'Spanish'),
    ('fr', 'French'),
    ('de', 'German'),
    ('zh-hans', 'Simplified Chinese'),
    ('ja', 'Japanese'),
    ('pt', 'Portuguese'),
    ('hi', 'Hindi'),
]

LOCALE_PATHS = [BASE_DIR / 'locale']

USE_I18N = True
USE_L10N = True

# LocaleMiddleware must be positioned after SessionMiddleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # ← Must be here
    'django.middleware.common.CommonMiddleware',
    # ... other middleware ...
]
```

### urls.py

```python
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

# All user-facing URLs wrapped with i18n_patterns
urlpatterns += i18n_patterns(
    path('', include('home.urls')),
    path('movies/', include('movies.urls')),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('translations/', include('translations.urls')),
    path("petitions/", include(("petitions.urls", "petitions"), namespace="petitions")),
    prefix_default_language=True
)
```

## Using the Translation API

### JavaScript Example

```javascript
// Translate book description from English to Spanish
fetch('/en/translations/translate/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        text: 'This is a fascinating science fiction novel.',
        source_language: 'en',
        target_language: 'es'
    })
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        console.log('Translation:', data.translated);
        console.log('Cached:', data.cached);
    }
});
```

### Python Example

```python
import requests
import json

def translate_text(text, source_lang='en', target_lang='es'):
    response = requests.post(
        'http://localhost:8000/en/translations/translate/',
        json={
            'text': text,
            'source_language': source_lang,
            'target_language': target_lang
        }
    )
    return response.json()

result = translate_text('Hello World', 'en', 'es')
print(result['translated'])  # Output: Hola Mundo
```

## Admin Interface

Access the admin interface to manage translations:

**URL:** `http://localhost:8000/admin/translations/`

### UserLanguagePreference Admin

- View all user language preferences
- Filter by language
- Search by username or email
- View creation and update timestamps

### CachedTranslation Admin

- Browse all cached translations
- Search by source or translated text
- Filter by language pair
- View text previews (first 50 chars)
- Manual cache management (add/delete entries)

## Testing

Run the translation test suite:

```bash
python manage.py test translations -v 2
```

**Test Coverage:**

1. **Model Tests (5 tests)**
   - Create language preference
   - Unique constraint verification
   - Default language setting
   - Create cached translation
   - Unique together constraint

2. **API Tests (8 tests)**
   - Translate with no text (error handling)
   - Translate same language (no-op)
   - Cached translation retrieval
   - Invalid JSON handling
   - Set valid preference
   - Set invalid preference
   - Get default preference
   - Get custom preference

**Expected Output:**
```
Ran 13 tests in 2.3s
OK
```

## Performance Considerations

### Caching Strategy

1. **First Request:** Translates via LibreTranslate API, stores in database
2. **Subsequent Requests:** Returns cached result (0-1ms vs 200-500ms)

### Database Indexes

The `CachedTranslation` model includes indexes on:
- `source_language` + `target_language` (for filtering language pairs)
- `unique_together` constraint on source/target/text (prevents duplicates)

### Query Optimization

```python
# Efficient lookup of cached translations
cached = CachedTranslation.objects.filter(
    source_language=source_lang,
    target_language=target_lang,
    source_text=source_text
).first()
```

## Troubleshooting

### Language Not Changing

**Problem:** Clicking language selector doesn't change the language.

**Solution:**
1. Check browser cookies are enabled
2. Verify LocaleMiddleware is in settings.py
3. Clear browser cache and cookies
4. Ensure you're using language-prefixed URLs

### Translation API Returns Error

**Problem:** "Translation API error" messages in logs.

**Solutions:**
1. Check internet connection (LibreTranslate is an external service)
2. Verify LibreTranslate API is online: `curl https://libretranslate.com/translate`
3. Check rate limiting - may need to implement request throttling
4. Fall back to cached translations if available

### Cached Translations Are Wrong

**Problem:** Old/incorrect cached translations are being used.

**Solution:**
1. Delete entries from CachedTranslation in admin panel
2. System will fetch fresh translation on next request
3. To clear all cache:
   ```bash
   python manage.py shell
   >>> from translations.models import CachedTranslation
   >>> CachedTranslation.objects.all().delete()
   ```

## Future Enhancements

1. **Batch Translation API**
   - Translate multiple texts in one request
   - Reduce round trips

2. **Automatic Template Translation**
   - Mark template strings with `{% trans %}` tags
   - Extract and manage translation files
   - Support plural forms and context

3. **Translation Quality Ratings**
   - Let users rate translation accuracy
   - Store user feedback in database
   - Use feedback for API provider selection

4. **Offline Translation**
   - Integrate offline translation library (e.g., Argos Translate)
   - Fallback to offline when API is unavailable

5. **Right-to-Left (RTL) Language Support**
   - Add CSS classes for Arabic, Hebrew, etc.
   - Auto-detect and apply RTL styling

6. **Translation Statistics**
   - Track most translated content
   - Monitor API usage and costs
   - Generate usage reports

## References

- [Django Internationalization Documentation](https://docs.djangoproject.com/en/5.0/topics/i18n/)
- [LibreTranslate API Documentation](https://github.com/LibreTranslate/LibreTranslate)
- [Django i18n Best Practices](https://docs.djangoproject.com/en/5.0/topics/i18n/translation/)
