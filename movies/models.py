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


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    rating = models.IntegerField(default=0)  # 0-5 star rating
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Review {self.id} on {self.movie.name} by {self.user}"