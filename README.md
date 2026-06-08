# Movie picker app

API для подбора фильмов, основанном на ваших рекомендациях или запросе.

---

## Функционал

- Регистрация и авторизация через JWT
- Просмотр каталога фильмов и жанров
- Оценка фильмов
- Персональные рекомендации на основе оценок
- Умный поиск по текстовому запросу (с переводом на английский)
- Автоматическое обновление рейтингов фильмов (Celery)
- Авто-поиск новинок (Celery Beat)
- Документация API (Swagger)

## Примененные технологии

- Python 3.12
- Django 6.0
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Docker / Docker Compose
- pytest
- Swagger (drf-spectacular)

## Установка и запуск

- Клонировать репозиторий
  ```bash
    git clone https://github.com/nktbezruk-art/movie-picker.git
    cd movie-picker
  ```

- Создать .env файл с переменными (перечень нужных в .env.example)
  
- Запустить приложение
  ```bash
    docker compose up --build
  ```

- Создать суперпользователя
  ```bash
    docker compose exec web python manage.py createsuperuser
  ```

- Открыть http://localhost:8000/api/docs/ - Swagger

## API Endpoints

| Метод   | URL                              | Описание                           | Требуется ли аутентификация |
|---------|----------------------------------|------------------------------------|-----------------------------|
| `GET`   | `/api/genres/`                   | Список всех жанров                 | Нет                         |
| `GET`   | `/api/genres/{id}/`              | Информация о жанре                 | Нет                         |
| `GET`   | `/api/movie_ratings/`            | Рейтинги пользователя              | Да                          |
| `POST`  | `/api/movie_ratings/`            | Создание/обновление рейтинга       | Да                          |
| `GET`   | `/api/movie_ratings/{id}/`       | Информация о рейтинге              | Да                          |
| `PUT`   | `/api/movie_ratings/{id}/`       | Полное обновление рейтинга         | Да                          |
| `PATCH` | `/api/movie_ratings/{id}/`       | Частичное обновление рейтинга      | Да                          |
| `DELETE`| `/api/movie_ratings/{id}/`       | Удаление рейтинга                  | Да                          |
| `GET`   | `/api/movies/`                   | Список всех фильмов                | Нет                         |
| `GET`   | `/api/movies/{id}/`              | Информация о фильме                | Нет                         |
| `GET`   | `/api/movies/recommended/`       | Персональные рекомендации          | Да                          |
| `POST`  | `/api/movies/smart_recommend/`   | Умный поиск по тексту              | Да                          |
| `POST`  | `/api/register/`                 | Регистрация нового пользователя    | Нет                         |
| `POST`  | `/api/token/`                    | Получение JWT токенов              | Нет                         |
| `POST`  | `/api/token/refresh/`            | Обновление JWT токена              | Нет                         |
| `GET`   | `/api/docs/`                     | Swagger UI                         | Нет                         |
| `GET`   | `/api/schema/`                   | OpenAPI схема                      | Нет                         |

## Тестирование

Для запуска тестов выполните команду
```bash
docker compose exec web pytest
```

Для запуска тестов с покрытием выполните команду
```bash
docker compose exec web pytest --cov=. --cov-report=term-missing
```

Использованные маркеры:
- views
- integration
- recommendations
- slow

---

## 👥 Разработчик

nktbezruk-art — Построено в процессе изучения Django REST Framework и Docker.