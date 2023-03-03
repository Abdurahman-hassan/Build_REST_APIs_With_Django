"""URLs for the watchlist app."""
from django.urls import path

from watchlist.api.views import \
    (
    # movie_list, movie_detail,
    MovieList, MovieDetail, StreamPlatformList, StreamPlatformDetail,
)

app_name = 'watchlist'
urlpatterns = [
    # function based views
    # path('list/', movie_list, name='movie_list'),
    # path('<int:movie_id>', movie_detail, name='movie_detail'),
    # class based views
    path('list/', MovieList.as_view(), name='movie_list'),
    path('<int:movie_id>', MovieDetail.as_view(), name='movie_detail'),
    path('stream/', StreamPlatformList.as_view(), name='streamplatform_list'),
    path('stream/<int:platform_id>/', StreamPlatformDetail.as_view(), name='streamplatform_detail'),
]
