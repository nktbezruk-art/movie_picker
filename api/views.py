import requests
from django.conf import settings
from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from main.models import Genre, Movie, MovieRating
from .serializers import GenreSerializer, MovieSerializer, MovieRatingSerializer, RegisterSerializer


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
        user = self.request.user
        high_ratings = MovieRating.objects.filter(user=user, rating__gte=7)
        rated_movies_ids = MovieRating.objects.filter(user=user).values_list('movie_id', flat=True)
        favourite_genres = Genre.objects.filter(movies__movierating__in=high_ratings)
        recommended_films = Movie.objects.filter(genres__in=favourite_genres).exclude(id__in=rated_movies_ids).order_by('-rating')[:10]
        serializer = self.get_serializer(recommended_films, many=True)
        return Response(serializer.data)
    
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