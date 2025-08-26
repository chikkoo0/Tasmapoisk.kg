from rest_framework import generics, filters
from .models import Movie, Review
from .serializers import MovieSerializer, ReviewSerializer


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