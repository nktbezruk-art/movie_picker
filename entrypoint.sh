#!/bin/bash
python manage.py migrate

COUNT=$(python manage.py shell -c "from main.models import Movie; print(Movie.objects.count())" 2>/dev/null | tail -1)

if [ "$COUNT" = "0" ]; then
    echo "Database is empty, fetching movies..."
    python manage.py fetch_movies
fi

python manage.py runserver 0.0.0.0:8000