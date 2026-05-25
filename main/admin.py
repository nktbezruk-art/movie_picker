from django.contrib import admin
from .models import Genre, Movie, MovieRating


# Register your models here.
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'rating')
    list_filter = ('genres', 'release_year', 'title', 'rating')
    search_fields = ('title',)


@admin.register(MovieRating)
class MovieRatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'rating', 'user')
    list_filter = ('rating', 'created_at')