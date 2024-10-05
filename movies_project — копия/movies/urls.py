from django.urls import path
from .views import MovieListCreateView, MovieDetailView

urlpatterns = [
    path('api/movies/', MovieListCreateView.as_view(), name='movie-list-create'),
    path('api/movies/<int:id>/', MovieDetailView.as_view(), name='movie-detail'),
]