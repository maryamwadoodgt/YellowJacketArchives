from django.contrib import admin
from .models import Movie, Review

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name', 'author', 'genre']
    list_display = ('id', 'name', 'author', 'publication_year', 'available')
    list_filter = ('available', 'publication_year', 'genre')
    list_editable = ('available',)

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)