from rest_framework import viewsets, permissions
from main.models import Genre, Movie, MovieRating
from .serializers import GenreSerializer, MovieSerializer, MovieRatingSerializer


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
        queryset = Genre.objects.all()
        serializer_class = GenreSerializer
        permission_classes = [permissions.AllowAny]
        

class MovieViewSet(viewsets.ReadOnlyModelViewSet):
        queryset = Movie.objects.all()
        serializer_class = MovieSerializer
        permission_classes = [permissions.AllowAny]
        

class MovieRatingViewSet(viewsets.ModelViewSet):
    queryset = MovieRating.objects.all()
    serializer_class = MovieRatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
       
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)