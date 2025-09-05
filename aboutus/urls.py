from django.urls import path
from .views import AboutUsListCreateView

urlpatterns = [
    path("aboutus/", AboutUsListCreateView.as_view(), name="aboutus-list"),
]