from django.contrib import admin
from .models import Movie, Review, LibraryBranch, Stock, MovieTranslation


class MovieTranslationInline(admin.TabularInline):
    """
    Inline editor for book translations within the Movie admin page.
    Allows admins to edit translations for all 8 languages directly from the book edit page.
    
    Fields:
    - language_code: Which language this translation is for (en, es, fr, de, zh-hans, ja, pt, hi)
    - name: Translated book title
    - description: Translated book description
    - author: Translated author name (optional)
    - genre: Translated genre (optional)
    """
    model = MovieTranslation
    extra = 1
    fields = ('language_code', 'name', 'author', 'genre', 'description')
    readonly_fields = ()


class MovieAdmin(admin.ModelAdmin):
    """
    Admin interface for managing books (movies) in the library.
    
    FEATURES:
    1. BOOK MANAGEMENT
       - Edit book titles, authors, genres, descriptions
       - Set publication year and availability status
       - Upload cover images
    
    2. TRANSLATION MANAGEMENT (8 Languages)
       - Click "Show translations" section to add/edit translations
       - Each book can have translations in: English, Spanish, French, German,
         Chinese (Simplified), Japanese, Portuguese, and Hindi
       - Click "+ Add another Movie Translation" to add a new language
    
    3. INVENTORY TRACKING
       - Mark books as available/checked out
       - Filter by availability and genre
       - Track publication years
    
    4. SEARCH & FILTERS
       - Search by book name, author, or genre
       - Filter by availability, publication year, genre
       - Sort by name, author, ID
    """
    ordering = ['name']
    search_fields = ['name', 'author', 'genre']
    list_display = ('id', 'name', 'author', 'publication_year', 'available')
    list_filter = ('available', 'publication_year', 'genre')
    list_editable = ('available',)
    list_display_links = ('id', 'name')
    inlines = [MovieTranslationInline]
    fieldsets = (
        ('Book Information', {
            'fields': ('name', 'author', 'genre', 'publication_year')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Availability', {
            'fields': ('available',)
        }),
        ('Cover Image', {
            'fields': ('image',)
        }),
    )


class MovieTranslationAdmin(admin.ModelAdmin):
    """
    Dedicated admin interface for managing all book translations across languages.
    
    USE THIS TO:
    - Add translations for a book in a specific language
    - Edit existing translations
    - View all translations by language
    - Bulk edit translations
    
    WORKFLOW:
    1. Click "Add Movie Translation" button
    2. Select the movie (book) to translate
    3. Select the language code (es, fr, de, zh-hans, ja, pt, hi)
    4. Enter translated values:
       - name: Book title in that language
       - author: Author name in that language
       - genre: Genre classification in that language
       - description: Book summary in that language
    5. Click "Save"
    
    IMPORTANT: Each book-language combination must be unique (can't have duplicate translations)
    """
    list_display = ('movie', 'language_code', 'name', 'author', 'genre')
    list_filter = ('language_code', 'movie')
    search_fields = ('movie__name', 'name', 'author')
    fieldsets = (
        ('Book & Language', {
            'fields': ('movie', 'language_code'),
            'description': 'Select the book and target language for this translation'
        }),
        ('Translated Content', {
            'fields': ('name', 'author', 'genre', 'description'),
            'description': 'Enter the translated values for this book in the selected language'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


class LibraryBranchAdmin(admin.ModelAdmin):
    """
    Admin interface for managing library branches (locations) used in the map feature.
    
    FEATURES:
    1. BRANCH INFORMATION
       - Branch name and address
       - Phone number for contact
    
    2. LOCATION DATA (for maps)
       - Latitude & Longitude coordinates for Leaflet map display
       - These are displayed on the book detail page interactive map
    
    3. INVENTORY LINKS
       - View which books are in stock at this branch
       - Manage stock quantities
    
    WORKFLOW FOR ADDING A BRANCH:
    1. Click "Add Library Branch"
    2. Enter branch name (e.g., "Main Library Downtown")
    3. Enter address (e.g., "123 Main St, Atlanta, GA 30308")
    4. Enter phone (e.g., "+1-404-123-4567")
    5. Enter latitude & longitude:
       - Use Google Maps or OpenStreetMap to find coordinates
       - Example: Georgia Tech = Latitude: 33.7756, Longitude: -84.3970
    6. Click "Save"
    
    The map will then display this branch as a marker when users visit book pages.
    """
    list_display = ('id', 'name', 'address', 'latitude', 'longitude', 'phone')
    search_fields = ('name', 'address')
    fieldsets = (
        ('Branch Details', {
            'fields': ('name', 'phone', 'address')
        }),
        ('Map Coordinates (Leaflet.js)', {
            'fields': ('latitude', 'longitude'),
            'description': 'Enter coordinates from Google Maps or OpenStreetMap. Format: 33.7756, -84.3970 (Georgia Tech example)'
        }),
    )


class StockAdmin(admin.ModelAdmin):
    """
    Admin interface for managing book inventory at library branches.
    
    FEATURES:
    1. INVENTORY TRACKING
       - See which books are at which branches
       - Track quantity of copies available
    
    2. RELATIONSHIP MANAGEMENT
       - Link books to branches
       - Update copy counts
    
    WORKFLOW:
    1. Click "Add Stock"
    2. Select the movie (book)
    3. Select the library branch
    4. Enter the count (number of copies available)
    5. Click "Save"
    
    IMPORTANT:
    - Each book-branch combination must be unique
    - Only branches with count > 0 appear on the map
    - Update counts to reflect current availability
    
    NOTE: Users see books on the map based on this stock data.
    If a book has count=0 at all branches, it won't show on any map.
    """
    list_display = ('id', 'movie', 'branch', 'count')
    list_filter = ('branch', 'movie')
    search_fields = ('movie__name', 'branch__name')
    fieldsets = (
        ('Inventory Assignment', {
            'fields': ('movie', 'branch', 'count')
        }),
    )


# Register all models with their admin interfaces
admin.site.register(Movie, MovieAdmin)
admin.site.register(MovieTranslation, MovieTranslationAdmin)
admin.site.register(Review)
admin.site.register(LibraryBranch, LibraryBranchAdmin)
admin.site.register(Stock, StockAdmin)