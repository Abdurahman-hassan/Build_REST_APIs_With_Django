from django.urls import path
from .models import Movie
from .views import movie_list, single_movie, movie_detail

urlpatterns = [
    path('fbv-movie-list', movie_list, name='fbv_watchlist'),
    path('fbv-movie-detail/<int:movie_id>', single_movie, name='fbv_movie_detail'),
    path('fbv-movie-more-detail/<int:movie_id>', movie_detail, name='fbv_movie_more_detail'),
]