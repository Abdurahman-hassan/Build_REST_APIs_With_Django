"""URLs for the watchlist app."""
from django.urls import path

from watchlist.views import (
    movie_list, movie_detail, single_movie
)

app_name = 'watchlist'
urlpatterns = [
    path('list/', movie_list, name='movie_list'),
    path('list/<int:movie_id>', single_movie, name='single_movie'),
    path('<int:movie_id>', movie_detail, name='movie_detail'),
]
