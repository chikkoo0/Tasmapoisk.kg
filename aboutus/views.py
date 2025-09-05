from drf_spectacular.utils import extend_schema
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import AboutUs
from .serializers import AboutUsSerializer


@extend_schema(summary='О нас', tags=['Movie'])
class AboutUsListCreateView(generics.ListCreateAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["email", "phone"]  # фильтры по полям
    search_fields = ["title", "description"]  # поиск по тексту
    ordering_fields = ["created_at", "title"]  # сортировка