"""Views for the API."""
from django.http import Http404
from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from watchlist.api.serializers import (MovieSerializer,
                                       StreamPlatformSerializer,
                                       ReviewSerializer,
                                       ManualMovieSerializer)
from watchlist.models import WatchMoviesList, StreamPlatform, Review
from django.http import JsonResponse
from watchlist.models import Movie


############################################################################################################
############################################################################################################
# function based views manual serialization/ deserialization
############################################################################################################

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
# function based views using a serializer class
############################################################################################################
@api_view(['GET', 'POST'])
def movie_list_using_serializer_class(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = ManualMovieSerializer(movies, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = ManualMovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # this serializer.data is the data that we just created of the return of the serializer created function
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'put', 'delete'])
def single_movie_using_serializer_class(request, movie_id):
    if request.method == 'GET':
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return Response(data={'Error': 'Movie not found'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = ManualMovieSerializer(movie)
        return Response(serializer.data)

    if request.method == 'PUT':
        # if we didn't get which movie to update and send it to serializer
        # it will create a new movie instead of updating the existing one
        # we need to send the movie id in the request {'id':1, ...}
        # or we can get which movie to update and send it to the serializer
        movie = Movie.objects.get(pk=movie_id)
        serializer = ManualMovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        movie = Movie.objects.get(pk=movie_id)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def movie_detail_using_serializer_class(request, movie_id):
    movie = Movie.objects.filter(pk=movie_id)
    # filter returns a queryset, so we need to convert it to a list
    serializer = ManualMovieSerializer(movie, many=True)
    # if I will use JsonResponse i need to pass safe=False
    return JsonResponse(serializer.data, safe=False)


############################################################################################################
############################################################################################################
# class based views
############################################################################################################

class MovieListAV(APIView):
    """List all movies with ApiViewClass."""

    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # this serializer.data is the data that we just created of the return of the serializer created function
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieDetailAV(APIView):
    """Retrieve, update or delete a movie instance."""

    def get_object(self, pk):
        try:
            movie = Movie.objects.get(pk=pk)
            return movie
        except Movie.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        movie = self.get_object(pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = self.get_object(pk)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = self.get_object(pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



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
