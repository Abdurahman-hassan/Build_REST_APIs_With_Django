"""URLs for the watchlist app."""
from django.urls import path, include
from rest_framework import routers

from watchlist.api.views import \
    (
    # movie_list, movie_detail,
    StreamPlatformList,
    StreamPlatformDetail,
    ReviewList,
    ReviewDetail,
    ReviewCreate,
    StreamPlatformVs,
    movie_list_manual_serializer_deserializer,
    single_movie_manual_serializer_deserializer,
    movie_detail_manual_serializer_deserializer,
    movie_list_using_serializer_class,
    single_movie_using_serializer_class,
    movie_detail_using_serializer_class, MovieListAV, MovieDetailAV
)

app_name = 'watchlist'

# routers help us to create urls for our models by combining the urls
router = routers.DefaultRouter()
# stream is the url name
router.register('stream', StreamPlatformVs, basename='streamplatform')
path('', include(router.urls)),

urlpatterns = [
    ##################################################################################
    ##################################################################################
    # function based views
    ##################################################################################
    # function based views
    # using manual serializer and deserializer
    # path('fbv-movie-list', movie_list_manual_serializer_deserializer, name='fbv_watchlist'),
    # path('fbv-movie-detail/<int:movie_id>', single_movie_manual_serializer_deserializer, name='fbv_movie_detail'),
    # path('fbv-movie-more-detail/<int:movie_id>', movie_detail_manual_serializer_deserializer,
    #      name='fbv_movie_more_detail'),
    ##################################################################################
    # using a serializer class
    path('fbv-movie-list', movie_list_using_serializer_class, name='fbv_watchlist'),
    path('fbv-movie-detail/<int:movie_id>', single_movie_using_serializer_class, name='fbv_movie_detail'),
    path('fbv-movie-more-detail/<int:movie_id>', movie_detail_using_serializer_class,
         name='fbv_movie_more_detail'),
    ##################################################################################
    ##################################################################################
    # class based views
    ##################################################################################
    path('cbv-movie-list', MovieListAV.as_view(), name='cbv_watchlist'),
    path('cbv-movie-detail/<int:pk>', MovieDetailAV.as_view(), name='cbv_movie_detail'),
    ##################################################################################


    # we will comment this because we will use routers
    # path('stream/', StreamPlatformList.as_view(), name='streamplatform-list'),
    # path('stream/<int:platform_id>/', StreamPlatformDetail.as_view(), name='streamplatform-detail'),

    # generic class based views with relationships
    path('stream/<int:watchlist_id>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('stream/<int:watchlist_id>/review/', ReviewList.as_view(), name='review-list'),
    path('stream/<int:watchlist_id>/review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
]
urlpatterns += router.urls
