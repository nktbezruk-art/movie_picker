# slim версия так как она меньшего размера и стабильней чем 3.14
FROM python:3.12-slim

# не создавать .pyc файлы (не создавать мусор)
ENV PYTHONDONTWRITEBYTECODE=1
# без буферзации логов и вывода логов в консоль в реальном времени
ENV PYTHONUNBUFFERED=1

WORKDIR /movie_picker_app

# для сборки psycopg2, если psycopg2-binary то не нужно
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# копирование и установка зависимостей идет перед копированием кода проекта
# чтоб экономить время на сборку приложения
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 0.0.0.0:8000 чтоб слушал весь порт 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]