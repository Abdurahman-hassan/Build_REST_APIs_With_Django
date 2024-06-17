"""Views for the API."""
from django.http import Http404
from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from watchlist.api.serializers import MovieSerializer, StreamPlatformSerializer, ReviewSerializer, ManualMovieSerializer
from watchlist.models import WatchMoviesList, StreamPlatform, Review

############################################################################################################
# function based views manual serialization/ deserialization
from django.http import JsonResponse
from watchlist.models import Movie


def movie_list_manual_serializer_deserializer(request):
    movies = Movie.objects.all()
    # all returns a queryset, so we need to convert it to a list
    print(movies.values('name', 'description'))
    data = {
        'movies': list(movies.values('name', 'description'))
    }
    return JsonResponse(data)


def single_movie_manual_serializer_deserializer(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    # get returns a single object, so we can access its attributes directly
    data = {
        'movie': {
            'name': movie.name,
            'description': movie.description,
        }
    }
    return JsonResponse(data)


def movie_detail_manual_serializer_deserializer(request, movie_id):
    movie = Movie.objects.filter(pk=movie_id)
    # filter returns a queryset, so we need to convert it to a list
    data = {
        'movie':
            list(movie.values('name', 'description'))
    }
    return JsonResponse(data)


############################################################################################################
############################################################################################################
# using a serializer class
@api_view()
def movie_list_using_serializer_class(request):
    movies = Movie.objects.all()
    serializer = ManualMovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view()
def single_movie_using_serializer_class(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    serializer = ManualMovieSerializer(movie)
    return Response(serializer.data)



def movie_detail_using_serializer_class(request, movie_id):
    movie = Movie.objects.filter(pk=movie_id)
    # filter returns a queryset, so we need to convert it to a list
    serializer = ManualMovieSerializer(movie, many=True)
    return JsonResponse(serializer.data, safe=False)


############################################################################################################

# We will use the generic class based views itself
# we don't need to define the get, post, put, delete methods
# it will be done automatically because it's inherited the mixins.


class ReviewCreate(generics.CreateAPIView):
    """Create a review,
       This class doesn't have a queryset because we don't need to get the reviews.
    """
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()

    #
    def perform_create(self, serializer):
        # the pk is the movie id
        watchlist_id = self.kwargs['watchlist_id']
        movie = WatchMoviesList.objects.get(pk=watchlist_id)

        user = self.request.user
        review_queryset = Review.objects.filter(watchlist=movie, reviewer=user)
        if review_queryset.exists():
            raise ValidationError('You have already reviewed this movie')
        # we need to pass the movie to the serializer to save it in the review model
        serializer.save(watchlist=movie, reviewer=user)


class ReviewList(generics.ListAPIView):
    """List all reviews."""
    # ListCreate will give us the get and post methods
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # we need to override the get_queryset method to filter the reviews by platform_id

    # watchlist is the related name of the foreign key in the Review model
    def get_queryset(self):
        watch_list = self.kwargs['watchlist_id']
        return Review.objects.filter(watchlist=watch_list)

    # or

    # def get_queryset(self):
    #     if self.kwargs.get('platform_id'):
    #         return Review.objects.filter(watchlist=self.kwargs.get('platform_id'))
    #     return Review.objects.all()
    #
    # # or
    # def get_queryset(self):
    #     pk = self.kwargs['platform_id']
    #     return Review.objects.filter(watchlist=pk) if pk else Review.objects.all()


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a review."""
    # RetrieveUpdateDestroy will give us the get, put, delete methods
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        watch_list = self.kwargs['watchlist_id']
        return Review.objects.filter(watchlist=watch_list)


# Mixins
# class ReviewDetail(mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.DestroyModelMixin,
#                    generics.GenericAPIView):
#     """Retrieve, update or delete a review."""
#
#     # These are attributes names and we can't change them
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
#
#
# class ReviewList(mixins.ListModelMixin,
#                  mixins.CreateModelMixin,
#                  generics.GenericAPIView):
#     """List all reviews."""
#
#     # These are attributes names and we can't change them
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# model viewset
class StreamPlatformVs(viewsets.ModelViewSet):
    """List all stream platforms."""
    queryset = StreamPlatform.objects.all()
    # serializer_class is a unique attribute name and we can't change it
    serializer_class = StreamPlatformSerializer


# ViewSets

# class StreamPlatformVs(viewsets.ViewSet):
#     """List all stream platforms."""
#
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         platform = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(platform)
#         return Response(serializer.data)
#
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def update(self, request, pk=None):
#         platform = StreamPlatform.objects.get(pk=pk)
#         serializer = StreamPlatformSerializer(platform, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def destroy(self, request, pk=None):
#         platform = StreamPlatform.objects.get(pk=pk)
#         platform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# API View

class StreamPlatformList(APIView):
    """List all stream platforms."""

    # add validation to the view
    def get(self, request):
        stream_platforms = StreamPlatform.objects.all()
        # we add context={'request': request} to get the url of the related objects in the serializer
        serializer = StreamPlatformSerializer(stream_platforms,
                                              many=True,
                                              context={'request': request})

        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetail(APIView):
    """Retrieve a stream platform."""

    def get_object(self, platform_id):
        try:
            platform = StreamPlatform.objects.get(pk=platform_id)
            return platform
        except StreamPlatform.DoesNotExist:
            raise Http404

    def get(self, request, platform_id):
        try:
            platform = self.get_object(platform_id)
        except Http404:
            return Response(data={'Error': 'Platform not found to retrieve.'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)

    def put(self, request, platform_id):
        try:
            platform = self.get_object(platform_id)
        except Http404:
            return Response(data={'Error': 'Platform not found to update.'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, platform_id):
        try:
            platform = self.get_object(platform_id)
        except Http404:
            return Response(data={'Error': 'Platform not found to delete.'},
                            status=status.HTTP_404_NOT_FOUND)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

