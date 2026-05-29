# import requests
# from django.conf import settings
from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from deep_translator import GoogleTranslator
from main.models import Genre, Movie, MovieRating
from .serializers import GenreSerializer, MovieSerializer, MovieRatingSerializer, RegisterSerializer
import logging
logger = logging.getLogger(__name__)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.AllowAny]
        

class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['get', ], permission_classes=[permissions.IsAuthenticated])
    def recommended(self, request):
        """
        Простая система рекоммендаций.
        Возвращает 10 рекомендованных фильмов.
        Любимые жанры определяются из высоких оценок (≥7).
        Исключает уже оценённые пользователем фильмы.
        """
        user = self.request.user
        high_ratings = MovieRating.objects.filter(user=user, rating__gte=7)
        rated_movies_ids = MovieRating.objects.filter(user=user).values_list('movie_id', flat=True)
        favourite_genres = Genre.objects.filter(movies__movierating__in=high_ratings)
        recommended_films = Movie.objects.filter(genres__in=favourite_genres).exclude(id__in=rated_movies_ids).distinct().order_by('-rating')[:10]
        if not recommended_films:
            recommended_films = Movie.objects.exclude(id__in=rated_movies_ids).order_by('-rating')[:10]
        serializer = self.get_serializer(recommended_films, many=True)
        return Response(serializer.data)
    
    
    @action(detail=False, methods=['post', ], permission_classes=[permissions.IsAuthenticated])
    def smart_recommend(self, request):
        """
        Умная система рекомендаций.
        Обрабатывает запрос пользователя переводит его на английский язык,
        ищет в нем название фильмов и жанры.
        Возвращает топ 10 фильмов, основываясь на полученных данных.
        Если не найдено ни одного фильма, возвращает топ 10 фильмов по рейтингу.
        """
        user = self.request.user
        rated_movies_ids = MovieRating.objects.filter(user=user).values_list('movie_id', flat=True)
        request_text = request.data.get('query', '')
        if not request_text:
            return Response({'error': 'No query provided'}, status=400)
        found_movies, found_genres = set(), set()
        try:
            translated_request = GoogleTranslator(source='ru', target='en').translate(request_text)
        except Exception:
            translated_request = request_text

        for movie in Movie.objects.all():
            if movie.title.lower() in translated_request.lower():
                found_movies.add(movie)
        
        for genre in Genre.objects.all():
            if genre.name.lower() in translated_request.lower():
                found_genres.add(genre)
            
        final_movie_set = found_movies

            
        for genre in found_genres:
            genre_movies = list(Movie.objects.filter(genres=genre))
            final_movie_set.update(genre_movies)
        
        
        # Если из запроса не будет найдено фильмов, вернется топ фильмов по рейтингу.
        # Срез не делается потому что может быть, что если срез возьмется сейчас, то будут только просмотренные фильмы,
        # которые отсеятся дальше, и будет возвращен пустой список.
        if not final_movie_set:
            final_movie_set = set(Movie.objects.order_by('-rating'))
        
        # Для того чтобы убрать уже оцененные фильмы
        final_movie_set = {m for m in final_movie_set if m.pk not in rated_movies_ids}

        serializer = self.get_serializer(
            sorted(final_movie_set, key=lambda m: m.rating or 0, reverse=True)[:10], many=True)
        return Response(serializer.data)
                
        
    # HuggingFace API недоступен, реалиуется позже

    # @action(detail=False, methods=['post', ], permission_classes=[permissions.IsAuthenticated])
    # def ai_recommended(self, request):
    #     API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
    #     headers = {"Authorization": f"Bearer {settings.HF_API_TOKEN}"}

    #    request_text = request.data.get('query', '')
    #    if not request_text:
    #         return Response({'error': 'No query provided'}, status=400)
    #     high_ratings = MovieRating.objects.filter(user=request.user, rating__gte=7)
    #     favourite_genres_names = Genre.objects.filter(movies__movierating__in=high_ratings).values_list('name', flat=True)
    #     favourite_movies_names = high_ratings.values_list('movie__title', flat=True)
        
    #     all_movies = Movie.objects.all()
    #     movies_text = "\n".join([
    #         f"- {m.title} (жанры: {', '.join(g.name for g in m.genres.all())}): {m.description[:100]}"
    #         for m in all_movies
    #    ])
    #     prompt = f"""
# Пользователь любит жанры: {', '.join(favourite_genres_names)}.
# Пользователь оценил высоко эти фильмы: {', '.join(favourite_movies_names)}.
# Запрос пользователя: {request_text}.

# Вот база фильмов с жанрами и описаниями:
# {movies_text}
# """
#        payload = {
#     "inputs": prompt,
#     "parameters": {"max_new_tokens": 100}
#     }
#         response = requests.post(API_URL, headers=headers, json=payload)
#         data = response.json()
#         return Response(data)
    
        
        

class MovieRatingViewSet(viewsets.ModelViewSet):
    queryset = MovieRating.objects.all()
    serializer_class = MovieRatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
       
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)