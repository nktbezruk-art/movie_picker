from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Movie(models.Model):
    title = models.CharField(max_length=300, unique=True)
    description = models.TextField(blank=True)
    release_year = models.IntegerField(null=True, blank=True)
    poster_url = models.URLField(blank=True)
    rating = models.FloatField(null=True)
    genres = models.ManyToManyField(Genre, related_name='movies')
    director = models.CharField(max_length=200, blank=True)
    actors = models.TextField(blank=True)
    runtime = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-rating', '-release_year']
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

class MovieRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} rated {self.movie.title}"
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'movie']
        verbose_name = 'Movie Rating'
        verbose_name_plural = 'Movie Ratings'