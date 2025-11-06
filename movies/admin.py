from django.contrib import admin
from .models import Movie, Review, Book

# Make the admin site explicitly focused on the Library
admin.site.site_header = 'Yellow Jacket Archives — Library Admin'
admin.site.site_title = 'Library Admin'
admin.site.index_title = 'Library Administration'

# Unregister Movie to avoid confusion (admin now focuses on Books/Library).
# If you still want Movie in admin, remove the unregister call below.
try:
    admin.site.unregister(Movie)
except Exception:
    # Movie may not be registered yet; ignore in that case.
    pass


class BookAdmin(admin.ModelAdmin):
    """Admin for Book: searchable and shows details required by user stories."""
    list_display = ('title', 'author', 'genre', 'publication_year', 'available')
    search_fields = ('title', 'author', 'genre')
    list_filter = ('genre', 'available', 'publication_year')
    ordering = ('title',)
    readonly_fields = ()


class ReviewAdmin(admin.ModelAdmin):
    search_fields = ('comment', 'user__username', 'movie__name')
    list_display = ('id', 'movie', 'user', 'date')


admin.site.register(Book, BookAdmin)
admin.site.register(Review, ReviewAdmin)