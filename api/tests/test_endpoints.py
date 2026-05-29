import pytest
from typing import cast
from rest_framework.response import Response


@pytest.mark.django_db
@pytest.mark.views
def test_get_movie_list(api_client):
    """
    Тест получения списка фильмов
    """
    response = cast(Response, api_client.get('/api/movies/'))
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.views
def test_get_one_movie(api_client, movie):
    """"
    Тест получения одного фильма
    """
    response = cast(Response, api_client.get(f'/api/movies/{movie.id}/'))
    assert response.status_code == 200
    assert response.json()['title'] == movie.title
    


@pytest.mark.django_db
@pytest.mark.views
def test_get_genre_list(api_client):
    """
    Тест получения списка жанров
    """
    response = cast(Response, api_client.get('/api/genres/'))
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.views
def test_get_one_genre(api_client, horror_genre):
    """
    Тест получения одного жанра
    """
    response = cast(Response, api_client.get(f'/api/genres/{horror_genre.id}/'))
    assert response.status_code == 200
    assert response.json()['name'] == horror_genre.name
    

@pytest.mark.django_db
@pytest.mark.views
def test_get_movie_ratings_list(api_client, user, good_movie_rating):
    """
    Тест получения рейтинга фильма.
    Проверяет оба случая: с авторизацией и без.
    """
    response = cast(Response, api_client.get('/api/movie_ratings/'))
    assert response.status_code == 401
    api_client.force_authenticate(user=user)
    response = cast(Response, api_client.get('/api/movie_ratings/'))
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.views
def test_post_movie_rating(api_client, user, movie):
    """
    Тест создания рейтинга фильма.
    Проверяет все случаи: неавторизрванность, невалидные данные, успешный сценарий.
    """
    response = cast(Response, api_client.post(
        '/api/movie_ratings/',
        {"rating": 10, "movie": movie.id})
                    )
    assert response.status_code == 401

    api_client.force_authenticate(user=user)

    response = cast(Response, api_client.post(
        '/api/movie_ratings/',
        {"rating": -1, "movie": movie.id})
                    )
    assert response.status_code == 400
    
    response = cast(Response, api_client.post(
        '/api/movie_ratings/',
        {"rating": 10, "movie": movie.id})
                    )
    assert response.status_code == 201


@pytest.mark.django_db
@pytest.mark.views
def test_api_register(api_client):
    """
    Тест регистрации пользователя.
    Проверяет все случаи: невалидные данные, успешный сценарий.
    """
    
    response = cast(
        Response,
        api_client.post('/api/register/', {'username': 'test', 'email': 'bad_email', 'password': 'test'})
    )
    assert response.status_code == 400
    
    response = cast(
        Response,
        api_client.post('/api/register/', {'username': 'test', 'email': 'goodemail@gmail.com', 'password': 'test'})
    )
    assert response.status_code == 400
    
    response = cast(
        Response,
        api_client.post('/api/register/', {'username': 'test', 'email': 'goodemail@gmail.com', 'password': 'test_password'})
    )
    assert response.status_code == 201
    

@pytest.mark.django_db
@pytest.mark.views
def test_api_token(api_client, user):
    """
    Тест получения токенов.
    """
    response = cast(
        Response,
        api_client.post('/api/token/', {'username': user.username, 'password': '12345678'})
    )
    assert response.status_code == 200
    assert 'access' in response.json()
    assert 'refresh' in response.json()
    

@pytest.mark.django_db
@pytest.mark.views
def test_api_refresh(api_client, user):
    """
    Тест обновления токенов.
    """
    response = cast(
        Response,
        api_client.post('/api/token/', {'username': user.username, 'password': '12345678'})
    )
    refresh = response.json()['refresh']
    
    response = cast(
        Response,
        api_client.post('/api/token/refresh/', {'refresh': refresh})
    )
    assert response.status_code == 200
    assert 'access' in response.json()