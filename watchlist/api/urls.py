"""URLs for the watchlist app."""
from django.urls import path

from watchlist.api.views import \
    (
    # movie_list, movie_detail,
    MovieList, MovieDetail, StreamPlatformList, StreamPlatformDetail, ReviewList, ReviewDetail, ReviewCreate,
)

app_name = 'watchlist'
urlpatterns = [
    # function based views
    # path('list/', movie_list, name='movie_list'),
    # path('<int:movie_id>', movie_detail, name='movie_detail'),
    # class based views
    path('list/', MovieList.as_view(), name='movie-list'),
    path('<int:movie_id>', MovieDetail.as_view(), name='movie-detail'),
    path('stream/', StreamPlatformList.as_view(), name='streamplatform-list'),
    path('stream/<int:platform_id>/', StreamPlatformDetail.as_view(), name='streamplatform-detail'),

    # generic class based views with relationships
    path('stream/<int:watchlist_id>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('stream/<int:watchlist_id>/review/', ReviewList.as_view(), name='review-list'),
    path('stream/<int:watchlist_id>/review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
]
