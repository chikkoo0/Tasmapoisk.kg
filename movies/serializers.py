from rest_framework import serializers
from .models import Movie, Review, Genre, Person, News, Contact, Favorite


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'biography', 'birth_date', 'photo', 'role']

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'created_at', 'image']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'email', 'phone', 'address', 'message', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'text', 'rating', 'created_at']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"

class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'year', 'genres', 'poster', 'trailer_url', 'reviews']


class FavoriteSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)  # для отображения полной информации о фильме
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(), source="movie", write_only=True
    )  # для добавления фильма в избранное по ID

    class Meta:
        model = Favorite
        fields = ["id", "movie", "movie_id"]

    def create(self, validated_data):
        user = self.context["request"].user
        return Favorite.objects.create(user=user, **validated_data)

