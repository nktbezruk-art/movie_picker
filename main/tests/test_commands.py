import pytest
import requests
from django.conf import settings


@pytest.mark.integration
@pytest.mark.slow
def test_fetch_movies():
    """
    Тест того, что команда обращается к API OMDB и того,
    что структура ответа именно такая, какая нам нужна для работы команды.
    """
    url = f'http://www.omdbapi.com/?t=Inception&y=2010&apikey={settings.OMDB_API_KEY}'
    response = requests.get(url)
    data = response.json()
    assert data['Response'] == 'True'
    assert 'Title' in data
    assert 'imdbRating' in data
    assert 'Genre' in data
    assert isinstance(data['Year'], str)
    assert data['Genre']
    
    # Русских заголовков в OMDB API нет, так что поиск по русскому названию
    # фильма должен вернуть 'Response': 'False'
    russian_title = 'Начало' 
    url = f'http://www.omdbapi.com/?t={russian_title}&y=2010&apikey={settings.OMDB_API_KEY}'
    response = requests.get(url)
    data = response.json()
    assert data['Response'] == 'False'