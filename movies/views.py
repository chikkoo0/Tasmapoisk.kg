import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.response import Response

from .models import Movie, Review, Genre, Person, News, Contact
from .serializers import MovieSerializer, ReviewSerializer, GenreSerializer, PersonSerializer, NewsSerializer, \
    ContactSerializer, FavoriteSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Favorite
from drf_spectacular.utils import extend_schema

class MovieFilter(django_filters.FilterSet):
    # Явное определение фильтра для поиска по полю genres__name
    genres_name = django_filters.CharFilter(
        field_name='genres__name',
        lookup_expr='iexact' # Используйте 'iexact' для точного совпадения без учета регистра
                            # или 'icontains' для поиска по частичному совпадению
    )

    class Meta:
        model = Movie
        # Здесь укажите только простые имена полей модели
        fields = ['year']

@extend_schema(summary='Список и поиск, фильтрация кино', tags=['Movie'])
class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MovieFilter
    filterset_fields = ['genres__name']  # фильтрация по жанру
    search_fields = ['title', 'description']
    ordering_fields = ['year']

@extend_schema(summary='Детальный просмотр,методы кино', tags=['Movie'])
class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


@extend_schema(summary='Генерация отзыва', tags=['Movie'])
class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        movie_id = self.kwargs['movie_id']
        serializer.save(movie_id=movie_id, user=self.request.user)
@extend_schema(summary='Актеры в кино', tags=['Movie'])
class PersonListView(generics.ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
@extend_schema(summary='Детальный просмотр актеров в кино', tags=['Movie'])
class PersonDetailView(generics.RetrieveAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
@extend_schema(summary='Новости', tags=['Movie'])
class NewsListView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
@extend_schema(summary='Детальный просмотр новостей', tags=['Movie'])
class NewsDetailView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
@extend_schema(summary='Контакты', tags=['Movie'])
class ContactInfoView(generics.ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
@extend_schema(summary='Поле поиска кино', tags=['Movie'])
class MovieSearchView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'genre']
@extend_schema(summary='Последние кино', tags=['Movie'])
class LatestMoviesView(generics.ListAPIView):
    queryset = Movie.objects.order_by('-year')[:10]
    serializer_class = MovieSerializer


from rest_framework import generics
from .models import Movie, Genre
from .serializers import MovieSerializer

@extend_schema(summary='Жанры кино', tags=['Movie'])
class MoviesByGenreView(generics.ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        # Эта проверка нужна только для drf-spectacular, чтобы предотвратить ошибку.
        if getattr(self, 'swagger_fake_view', False):
            return Movie.objects.none()

        genre_name = self.kwargs['genre']

        # 1. Сначала находим объект жанра. Используем __iexact здесь, потому что 'name' — это строковое поле.
        try:
            genre_obj = Genre.objects.get(name__iexact=genre_name)
        except Genre.DoesNotExist:
            # Если жанр не найден, возвращаем пустой набор данных.
            return Movie.objects.none()

        # 2. Фильтруем фильмы, передавая сам объект жанра.
        # Django автоматически использует первичный ключ (ID) для сопоставления.
        return Movie.objects.filter(genre=genre_obj)


@extend_schema(summary='Избаррнные кино', tags=['Movie'])
class FavoriteListView(generics.ListAPIView):
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Favorite.objects.none()
        return Movie.objects.filter(favorite__user=self.request.user)
@extend_schema(summary='Добавление избранных кино', tags=['Movie'])
class AddFavoriteView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()

    def post(self, request, movie_id):
        Favorite.objects.get_or_create(user=request.user, movie_id=movie_id)
        return Response({"status": "added to favorites"})

