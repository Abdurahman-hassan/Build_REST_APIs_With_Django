"""Views for the API."""
from django.http import Http404
from rest_framework import status, generics, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from watchlist.api.serializers import MovieSerializer, StreamPlatformSerializer, ReviewSerializer
from watchlist.models import WatchMoviesList, StreamPlatform, Review


# We will use the generic class based views itself
# we don't need to define the get, post, put, delete methods
# it will be done automatically because it's inherited the mixins.


class ReviewCreate(generics.CreateAPIView):
    """Create a review,
       This class doesn't have a queryset because we don't need to get the reviews.
    """
    serializer_class = ReviewSerializer

    #
    def perform_create(self, serializer):
        # the pk is the movie id
        watchlist_id = self.kwargs['watchlist_id']
        movie = WatchMoviesList.objects.get(pk=watchlist_id)
        # we need to pass the movie to the serializer to save it in the review model
        serializer.save(watchlist=movie)


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


# ViewSets

class StreamPlatformVs(viewsets.ViewSet):
    """List all stream platforms."""

    def list(self, request):
        queryset = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = StreamPlatform.objects.all()
        platform = get_object_or_404(queryset, pk=pk)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)

    def create(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
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


# class based view
class MovieList(APIView):
    """List all movies."""

    def get(self, request):
        movies = WatchMoviesList.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieDetail(APIView):
    """Retrieve a movie."""

    def get_object(self, movie_id):
        try:
            movie = WatchMoviesList.objects.get(pk=movie_id)
            return movie
        except WatchMoviesList.DoesNotExist:
            return Response(data={'Error': 'Movie not found'},
                            status=status.HTTP_404_NOT_FOUND)

    # def get(self, request, movie_id):
    #     movie = self.get_object(movie_id)
    #     serializer = MovieSerializer(movie)
    #     return Response(serializer.data)

    def get(self, request, movie_id):
        try:
            movie = WatchMoviesList.objects.get(pk=movie_id)
        except WatchMoviesList.DoesNotExist:
            return Response(data={'Error': 'Movie not found'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def put(self, request, movie_id):
        try:
            movie = WatchMoviesList.objects.get(pk=movie_id)
        except WatchMoviesList.DoesNotExist:
            return Response(data={'Error': 'Movie not found'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, movie_id):
        try:
            movie = WatchMoviesList.objects.get(pk=movie_id)
        except WatchMoviesList.DoesNotExist:
            return Response(data={'Error': 'Movie not found'},
                            status=status.HTTP_404_NOT_FOUND)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# method view
# @api_view(['GET', 'POST'])
# def movie_list(request):
#     """List all movies."""
#     if request.method == 'GET':
#         movies = WatchMoviesList.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
#
#     if request.method == 'POST':
#         # get data from user i don't need to get data from db
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#             # this serializer.data is the data that
#             # we just created of the return of the serializer created function
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_detail(request, movie_id):
#     """Retrieve a movie."""
#     if request.method == 'GET':
#         try:
#             movie = WatchMoviesList.objects.get(pk=movie_id)
#         except WatchMoviesList.DoesNotExist:
#             return Response(data={'Error': 'Movie not found'},
#                             status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
#
#     if request.method == 'PUT':
#         try:
#             movie = WatchMoviesList.objects.get(pk=movie_id)
#         except WatchMoviesList.DoesNotExist:
#             return Response(data={'Error': 'Movie not found'},
#                             status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     if request.method == 'DELETE':
#         try:
#             movie = WatchMoviesList.objects.get(pk=movie_id)
#         except WatchMoviesList.DoesNotExist:
#             return Response(data={'Error': 'Movie not found'},
#                             status=status.HTTP_404_NOT_FOUND)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
