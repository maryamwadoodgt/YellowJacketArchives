import json
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import UserLanguagePreference, CachedTranslation


# LibreTranslate API endpoint (free, public API - no key required)
LIBRETRANSLATE_API = "https://libretranslate.com/translate"


def translate_text(source_text, source_lang, target_lang):
    """
    Translate text using LibreTranslate API with caching.
    Returns translated text or original text if translation fails.
    """
    # Check if translation is already cached
    cached = CachedTranslation.objects.filter(
        source_language=source_lang,
        target_language=target_lang,
        source_text=source_text
    ).first()
    
    if cached:
        return cached.translated_text

    try:
        response = requests.post(
            LIBRETRANSLATE_API,
            json={
                "q": source_text,
                "source": source_lang,
                "target": target_lang,
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            translated_text = result.get('translatedText', source_text)
            
            # Cache the translation
            CachedTranslation.objects.create(
                source_language=source_lang,
                target_language=target_lang,
                source_text=source_text,
                translated_text=translated_text
            )
            
            return translated_text
    except requests.exceptions.RequestException as e:
        print(f"Translation API error: {e}")
    
    # Return original text if translation fails
    return source_text


@csrf_exempt  # CSRF exempt for API requests from frontend
@require_http_methods(["POST"])
def translate_api(request):
    """
    API endpoint for translating text.
    POST /translations/translate/
    
    Request body:
    {
        "text": "string to translate",
        "source_language": "en",
        "target_language": "es"
    }
    
    Response:
    {
        "success": true,
        "original": "string to translate",
        "translated": "cadena para traducir",
        "source_language": "en",
        "target_language": "es"
    }
    """
    try:
        data = json.loads(request.body)
        source_text = data.get('text', '').strip()
        source_lang = data.get('source_language', 'en')
        target_lang = data.get('target_language', 'en')
        
        if not source_text:
            return JsonResponse({
                'success': False,
                'error': 'No text provided'
            }, status=400)
        
        # If source and target are the same, return original
        if source_lang == target_lang:
            return JsonResponse({
                'success': True,
                'original': source_text,
                'translated': source_text,
                'source_language': source_lang,
                'target_language': target_lang,
                'cached': False
            })
        
        # Translate the text
        translated_text = translate_text(source_text, source_lang, target_lang)
        
        return JsonResponse({
            'success': True,
            'original': source_text,
            'translated': translated_text,
            'source_language': source_lang,
            'target_language': target_lang,
            'cached': CachedTranslation.objects.filter(
                source_language=source_lang,
                target_language=target_lang,
                source_text=source_text
            ).exists()
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required(login_url='accounts.login')
def set_language_preference(request):
    """
    Set user's preferred language.
    POST /translations/set-preference/
    
    Request body:
    {
        "language": "es"
    }
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            language = data.get('language', 'en')
            
            # Validate language choice
            valid_languages = ['en', 'es', 'fr', 'de', 'zh-hans', 'ja', 'pt', 'hi']
            if language not in valid_languages:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid language'
                }, status=400)
            
            # Update or create user preference
            preference, created = UserLanguagePreference.objects.get_or_create(
                user=request.user
            )
            preference.preferred_language = language
            preference.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Language preference updated',
                'language': language
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Method not allowed'
    }, status=405)


@login_required(login_url='accounts.login')
def get_language_preference(request):
    """
    Get user's preferred language.
    GET /translations/get-preference/
    """
    try:
        preference = UserLanguagePreference.objects.get(user=request.user)
        language = preference.preferred_language
    except UserLanguagePreference.DoesNotExist:
        language = 'en'
    
    return JsonResponse({
        'success': True,
        'language': language
    })
