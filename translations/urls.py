from django.urls import path
from . import views

urlpatterns = [
    # Translation API endpoints
    path('translate/', views.translate_api, name='translate'),
    path('set-preference/', views.set_language_preference, name='set_preference'),
    path('get-preference/', views.get_language_preference, name='get_preference'),
]
