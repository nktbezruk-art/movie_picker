import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from main.models import Movie, Genre, MovieRating


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='testuser',
        email='test@gmail.com',
        password='12345678'
        )


@pytest.fixture
def action_genre(db):
    return Genre.objects.create(name="Action")


@pytest.fixture
def horror_genre(db):
    return Genre.objects.create(name="Horror")


@pytest.fixture
def movie(db, action_genre, horror_genre):
    movie = Movie.objects.create(
        title="Test",
        description='Description of a test movie',
        release_year=2020,
        rating=9.0,
        director="John Doe",
        runtime='120 minutes',
        country='USA',
        )
    movie.genres.set([horror_genre, action_genre])
    return movie


@pytest.fixture
def extra_movies(db, action_genre, horror_genre):
    movies = []
    for i in range(3):
        m = Movie.objects.create(title=f"Extra Movie {i}", rating=8.0)
        m.genres.add(action_genre, horror_genre)
        movies.append(m)
    return movies


@pytest.fixture
def good_movie_rating(db, movie, user):
    return MovieRating.objects.create(
        user=user,
        movie=movie,
        rating=9,
    )
    
    
@pytest.fixture
def bad_movie_rating(db, movie, user):
    return MovieRating.objects.create(
        user=user,
        movie=movie,
        rating=2,
    )