from django.urls import path
from .views import MovieListView, MovieDetailView, ReviewCreateView

urlpatterns = [
    path('movies/', MovieListView.as_view(), name="movie-list"),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name="movie-detail"),
    path('movies/<int:movie_id>/review/', ReviewCreateView.as_view(), name="review-create"),
]