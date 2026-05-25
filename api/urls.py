from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import GenreViewSet, MovieViewSet, MovieRatingViewSet


router = DefaultRouter()

router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'movies', MovieViewSet, basename='movies')
router.register(r'movie_ratings', MovieRatingViewSet, basename='movie_ratings')

app_name = 'api'


urlpatterns = [
    path('', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api:schema'), name='swagger-ui'),
]