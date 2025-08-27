from rest_framework import generics, filters
from rest_framework.response import Response

from .models import Movie, Review
from .serializers import MovieSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Favorite

class MovieListView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'genre']
    ordering_fields = ['year', 'title']

class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        movie_id = self.kwargs.get("movie_id")
        serializer.save(user=self.request.user, movie_id=movie_id)

class MovieSearchView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'genre']

class LatestMoviesView(generics.ListAPIView):
    queryset = Movie.objects.order_by('-year')[:10]
    serializer_class = MovieSerializer

class MoviesByGenreView(generics.ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        genre = self.kwargs['genre']
        return Movie.objects.filter(genre__iexact=genre)



class FavoriteListView(generics.ListAPIView):
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Movie.objects.filter(favorite__user=self.request.user)

class AddFavoriteView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, movie_id):
        Favorite.objects.get_or_create(user=request.user, movie_id=movie_id)
        return Response({"status": "added to favorites"})