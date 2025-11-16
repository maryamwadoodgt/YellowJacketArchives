import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.test.utils import override_settings
from .models import UserLanguagePreference, CachedTranslation


class UserLanguagePreferenceTests(TestCase):
    """Test UserLanguagePreference model."""
    
    def setUp(self):
        """Create test user."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_language_preference(self):
        """Test creating a language preference for a user."""
        pref = UserLanguagePreference.objects.create(
            user=self.user,
            preferred_language='es'
        )
        self.assertEqual(pref.preferred_language, 'es')
        self.assertEqual(pref.user.username, 'testuser')
    
    def test_user_language_preference_unique(self):
        """Test that each user can only have one language preference."""
        UserLanguagePreference.objects.create(
            user=self.user,
            preferred_language='es'
        )
        # Try to create another for same user should fail on save due to OneToOne
        with self.assertRaises(Exception):
            UserLanguagePreference.objects.create(
                user=self.user,
                preferred_language='fr'
            )
    
    def test_default_language(self):
        """Test default language is English."""
        pref = UserLanguagePreference.objects.create(user=self.user)
        self.assertEqual(pref.preferred_language, 'en')


class CachedTranslationTests(TestCase):
    """Test CachedTranslation model."""
    
    def test_create_cached_translation(self):
        """Test creating a cached translation."""
        cached = CachedTranslation.objects.create(
            source_language='en',
            target_language='es',
            source_text='Hello',
            translated_text='Hola'
        )
        self.assertEqual(cached.source_text, 'Hello')
        self.assertEqual(cached.translated_text, 'Hola')
    
    def test_unique_together_constraint(self):
        """Test unique constraint on source/target/text combination."""
        CachedTranslation.objects.create(
            source_language='en',
            target_language='es',
            source_text='Hello',
            translated_text='Hola'
        )
        # Try to create duplicate should fail
        with self.assertRaises(Exception):
            CachedTranslation.objects.create(
                source_language='en',
                target_language='es',
                source_text='Hello',
                translated_text='Hola'
            )


class TranslationAPITests(TestCase):
    """Test translation API endpoints."""
    
    def setUp(self):
        """Set up test client and user."""
        self.client = Client(enforce_csrf_checks=False)  # Disable CSRF for API tests
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        # Pre-populate some cached translations
        CachedTranslation.objects.create(
            source_language='en',
            target_language='es',
            source_text='Hello World',
            translated_text='Hola Mundo'
        )
    
    def test_translate_api_no_text(self):
        """Test translation endpoint with no text."""
        response = self.client.post(
            '/en/translations/translate/',
            data=json.dumps({
                'text': '',
                'source_language': 'en',
                'target_language': 'es'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
    
    def test_translate_api_same_language(self):
        """Test translation when source and target are the same."""
        response = self.client.post(
            '/en/translations/translate/',
            data=json.dumps({
                'text': 'Hello',
                'source_language': 'en',
                'target_language': 'en'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['original'], 'Hello')
        self.assertEqual(data['translated'], 'Hello')
    
    def test_translate_api_cached_translation(self):
        """Test that cached translations are returned."""
        response = self.client.post(
            '/en/translations/translate/',
            data=json.dumps({
                'text': 'Hello World',
                'source_language': 'en',
                'target_language': 'es'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['translated'], 'Hola Mundo')
        self.assertTrue(data['cached'])
    
    def test_translate_api_invalid_json(self):
        """Test translation endpoint with invalid JSON."""
        response = self.client.post(
            '/en/translations/translate/',
            data='invalid json',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
    
    def test_set_preference_valid_language(self):
        """Test setting a valid language preference."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            '/en/translations/set-preference/',
            data=json.dumps({'language': 'es'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        
        # Verify preference was saved
        pref = UserLanguagePreference.objects.get(user=self.user)
        self.assertEqual(pref.preferred_language, 'es')
    
    def test_set_preference_invalid_language(self):
        """Test setting an invalid language preference."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            '/en/translations/set-preference/',
            data=json.dumps({'language': 'invalid'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
    
    def test_get_preference_default(self):
        """Test getting language preference when none is set."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/en/translations/get-preference/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['language'], 'en')
    
    def test_get_preference_custom(self):
        """Test getting a custom language preference."""
        UserLanguagePreference.objects.create(
            user=self.user,
            preferred_language='fr'
        )
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/en/translations/get-preference/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['language'], 'fr')
