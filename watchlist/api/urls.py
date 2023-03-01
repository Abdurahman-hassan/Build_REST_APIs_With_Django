"""URLs for the watchlist app."""
from django.urls import path

from watchlist.api.views import (
    movie_list, movie_detail
)

app_name = 'watchlist'
urlpatterns = [
    path('list/', movie_list, name='movie_list'),
    path('<int:movie_id>', movie_detail, name='movie_detail'),
]
