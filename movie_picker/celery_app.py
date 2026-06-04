import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_picker.settings')

app = Celery('movie_picker')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()