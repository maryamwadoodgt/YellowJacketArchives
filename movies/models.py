from django.db import models
from django.conf import settings


class Movie(models.Model):
    """Represents a book in the library domain.

    The model name `Movie` is retained to avoid renaming the existing DB table.
    Fields describe book attributes: title (name), author, genre, summary (description),
    publication_year and availability.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    publication_year = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='movie_images/', blank=True, null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} - {self.name}"

    def get_translated_name(self, language_code):
        """Get the translated name for a given language, or fallback to English."""
        translation = self.translations.filter(language_code=language_code).first()
        if translation:
            return translation.name
        return self.name

    def get_translated_description(self, language_code):
        """Get the translated description for a given language, or fallback to English."""
        translation = self.translations.filter(language_code=language_code).first()
        if translation:
            return translation.description
        return self.description

    def get_translated_author(self, language_code):
        """Get the translated author for a given language, or fallback to English."""
        translation = self.translations.filter(language_code=language_code).first()
        if translation and translation.author:
            return translation.author
        return self.author

    def get_translated_genre(self, language_code):
        """Get the translated genre for a given language, or fallback to English."""
        translation = self.translations.filter(language_code=language_code).first()
        if translation and translation.genre:
            return translation.genre
        return self.genre


class MovieTranslation(models.Model):
    """Stores translations of movie titles, descriptions, author, and genre for different languages."""
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='translations')
    language_code = models.CharField(
        max_length=10,
        choices=[
            ('en', 'English'),
            ('es', 'Spanish'),
            ('fr', 'French'),
            ('de', 'German'),
            ('zh-hans', 'Chinese (Simplified)'),
            ('ja', 'Japanese'),
            ('pt', 'Portuguese'),
            ('hi', 'Hindi'),
        ]
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    author = models.CharField(max_length=255, blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('movie', 'language_code')
        verbose_name = 'Movie Translation'
        verbose_name_plural = 'Movie Translations'

    def __str__(self):
        language_names = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'zh-hans': 'Chinese (Simplified)',
            'ja': 'Japanese',
            'pt': 'Portuguese',
            'hi': 'Hindi',
        }
        language_display = language_names.get(self.language_code, self.language_code)
        return f"{self.movie.name} - {language_display}"


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    rating = models.IntegerField(default=0)  # 0-5 star rating
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Review {self.id} on {self.movie.name} by {self.user}"


class LibraryBranch(models.Model):
    """Represents a physical library branch where movies/books may be held."""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=512, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.id})"


class Stock(models.Model):
    """Tracks how many copies of a Movie are available at a given LibraryBranch."""
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='stocks')
    branch = models.ForeignKey(LibraryBranch, on_delete=models.CASCADE, related_name='stocks')
    count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('movie', 'branch')

    def __str__(self):
        return f"{self.movie.name} @ {self.branch.name}: {self.count}"