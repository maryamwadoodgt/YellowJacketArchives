from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')

    def __str__(self):
        return str(self.id) + ' - ' + self.name

class Book(models.Model):
    """A simple Book model to power library search and detail views."""
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100, blank=True)
    summary = models.TextField(blank=True)
    publication_year = models.IntegerField(null=True, blank=True)
    available = models.BooleanField(default=True)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='movie_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.title} by {self.author}"
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name