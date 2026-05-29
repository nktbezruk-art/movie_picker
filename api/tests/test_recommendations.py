import pytest
from typing import cast
from rest_framework.response import Response


@pytest.mark.django_db
@pytest.mark.views
@pytest.mark.recommendations
def test_simple_recommendations(api_client, user, extra_movies, good_movie_rating):
    """
    Тест простой системы рекоммендаций.
    Проверяет случаи неавторизованного пользователя и авторизованного.
    """
    response = cast(Response, api_client.get("/api/movies/recommended/"))
    assert response.status_code == 401

    api_client.force_authenticate(user=user)

    response = cast(Response, api_client.get("/api/movies/recommended/"))
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3


@pytest.mark.django_db
@pytest.mark.views
@pytest.mark.recommendations
def test_smart_recommendations(api_client, user, movie, extra_movies, good_movie_rating):
    response = cast(Response, api_client.get("/api/movies/smart_recommend/"))
    assert response.status_code == 401
    
    api_client.force_authenticate(user=user)
    response = cast(
        Response,
        api_client.post("/api/movies/smart_recommend/", {"query": ""}))
    assert response.status_code == 400
    response = api_client.post('/api/movies/smart_recommend/', {'query': 'Action'})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3
    
    # Этот блок проверяет что если из текста запроса
    # не будет найдено фильмов то возвратятся топ фильмы по рейтингу
    response = api_client.post('/api/movies/smart_recommend/', {'query': 'Something random'})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3
