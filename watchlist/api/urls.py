"""URLs for the watchlist app."""
from django.urls import path, include
from rest_framework import routers

from watchlist.api.views import \
    (
    # movie_list, movie_detail,
    # StreamPlatformList,
    # StreamPlatformDetail,
    ReviewList,
    ReviewDetail,
    ReviewCreate,
    StreamPlatformVs,
    watch_list_manual_serializer_deserializer,
    single_watch_list_manual_serializer_deserializer,
    watch_list_detail_manual_serializer_deserializer,
    watch_list_using_serializer_class,
    single_watch_list_using_serializer_class,
    watch_list_detail_using_serializer_class, WatchListAV, WatchListDetailAV, StreamPlatformAV, StreamPlatformDetailAV
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
    # using manual serializer and deserializer
    # path('fbv-watchlist-list', watch_list_manual_serializer_deserializer, name='fbv_watchlist'),
    # path('fbv-watchlist-detail/<int:movie_id>', single_watch_list_manual_serializer_deserializer, name='fbv_movie_detail'),
    # path('fbv-watchlist-more-detail/<int:movie_id>', watch_list_detail_manual_serializer_deserializer,
    #      name='fbv_movie_more_detail'),
    ##################################################################################
    ##################################################################################
    # using a serializer class
    path('fbv-watchlist-list', watch_list_using_serializer_class, name='fbv_watchlist'),
    path('fbv-watchlist-detail/<int:movie_id>', single_watch_list_using_serializer_class, name='fbv_movie_detail'),
    path('fbv-watchlist-more-detail/<int:movie_id>', watch_list_detail_using_serializer_class,
         name='fbv_movie_more_detail'),
    ##################################################################################
    ##################################################################################
    # class based views
    ##################################################################################
    path('list/', WatchListAV.as_view(), name='watchlist-list'),
    path('list/<int:pk>/', WatchListDetailAV.as_view(), name='watchlist-detail'),
    path('stream/', StreamPlatformAV.as_view(), name='streamplatform-list'),
    path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(), name='streamplatform-detail'),

    # generic class based views with relationships
    path('stream/<int:watchlist_id>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('stream/<int:watchlist_id>/review/', ReviewList.as_view(), name='review-list'),
    path('stream/<int:watchlist_id>/review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
]
urlpatterns += router.urls
