from django.urls import path
from .views import MovieListView, MovieDetailView, ReviewCreateView, MovieSearchView, LatestMoviesView, \
    MoviesByGenreView, FavoriteListView, AddFavoriteView, PersonListView, PersonDetailView, NewsListView, \
    NewsDetailView, ContactInfoView, CommentListCreateView

urlpatterns = [
    path('movies/', MovieListView.as_view(), name="movie-list"),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name="movie-detail"),
    path('movies/<int:movie_id>/review/', ReviewCreateView.as_view(), name="review-create"),
    path('movies/search/', MovieSearchView.as_view(), name="movie-search"),
    path('movies/latest/', LatestMoviesView.as_view(), name="latest-movies"),
    path('movies/genre/<str:genre>/', MoviesByGenreView.as_view(), name="movies-by-genre"),
    path('favorites/', FavoriteListView.as_view(), name="favorite-list"),
    path('favorites/add/<int:movie_id>/', AddFavoriteView.as_view(), name="favorite-add"),
    path('people/', PersonListView.as_view(), name='person-list'),
    path('people/<int:pk>/', PersonDetailView.as_view(), name='person-detail'),

    # 📰 Новости
    path('news/', NewsListView.as_view(), name='news-list'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news-detail'),

    # 📞 Контакты
    path('contacts/', ContactInfoView.as_view(), name='contacts'),
    path("movies/<int:movie_id>/comments/", CommentListCreateView.as_view(), name="movie-comments"),
]