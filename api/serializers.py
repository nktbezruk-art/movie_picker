from rest_framework import serializers
from main.models import Genre, Movie, MovieRating


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        


class MovieRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieRating
        fields = '__all__'
        read_only_fields = ['user', 'created_at']
        depth = 1
