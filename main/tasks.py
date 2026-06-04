import requests
from datetime import datetime
from celery import shared_task
from .models import Movie, Genre
from django.conf import settings


@shared_task
def update_ratings():
    updated_count = 0
    for movie in Movie.objects.all():
        response = requests.get(f'http://www.omdbapi.com/?t={movie.title}&y={movie.release_year}&apikey={settings.OMDB_API_KEY}')
        data = response.json()
        if data.get('Response') != 'True':
            continue
        rating_str = data.get('imdbRating', 'N/A')
        rating = float(rating_str) if rating_str != 'N/A' else None
        movie.rating = rating
        movie.save(update_fields=['rating'])
        updated_count += 1
    print(f'Updated {updated_count} movies')


@shared_task
def fetch_new_movies():
    new_movies = 0
    current_year = datetime.now().year
    response = requests.get(f'http://www.omdbapi.com/?s=movie&y={current_year}&apikey={settings.OMDB_API_KEY}')
    data = response.json()
    for item in data.get('Search', []):
        title = item.get('Title')
        year = item.get('Year')
        exists = Movie.objects.filter(title=title, release_year=year).exists()
        if not exists:
            response = requests.get(f'http://www.omdbapi.com/?t={title}&y={year}&apikey={settings.OMDB_API_KEY}')
            movie_data = response.json()
            if movie_data.get('Response') != 'True':
                continue
            rating_str = movie_data.get('imdbRating', 'N/A')
            rating = float(rating_str) if rating_str != 'N/A' else None
            movie, _ = Movie.objects.update_or_create(
                title=movie_data['Title'],
                defaults={
                    'description': movie_data.get('Plot', ''),
                    'release_year': int(movie_data.get('Year', 0)) if movie_data.get('Year', '').isdigit() else None,
                    'poster_url': movie_data.get('Poster', ''),
                    'rating': rating,
                    'director': movie_data.get('Director', ''),
                    'actors': movie_data.get('Actors', ''),
                    'runtime': movie_data.get('Runtime', ''),
                    'country': movie_data.get('Country', ''),
                }
            )
            genre_string = movie_data.get('Genre', '')
            for genre_name in genre_string.split(','):
                genre_name = genre_name.strip()
                if genre_name:
                    genre, _ = Genre.objects.update_or_create(name=genre_name)
                    movie.genres.add(genre)
            new_movies += 1
    print(f'Created {new_movies} new movies')
            