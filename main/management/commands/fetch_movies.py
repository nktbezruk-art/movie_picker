import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from main.models import Genre, Movie
from main.movie_list import MOVIES

class Command(BaseCommand):
    help = 'Команда заполнения базы данных фильмами со стороннего сервиса'
    API_KEY = settings.OMDB_API_KEY

    def handle(self, *args, **options):
        """
        Команда заполнения базы данных фильмами и жанрами.
        Список названий фильмов указан в main.movie_list.MOVIES.
        Заполнение происходит запросом к API OMDB.
        После выполнения команды в консоли выводится количество добавленных фильмов и жанров.
        """
        
        for title, year in MOVIES:
            response = requests.get(f'http://www.omdbapi.com/?t={title}&y={year}&apikey={Command.API_KEY}')
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
            
        self.stdout.write(self.style.SUCCESS(f'Добавлено {Movie.objects.count()} фильмов, {Genre.objects.count()} жанров'))
