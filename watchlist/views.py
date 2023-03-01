"""Views for the watchlist app."""
from django.http import JsonResponse

from watchlist.models import Movie


def movie_list(request):
    movies = Movie.objects.all()
    print(movies.values('title', 'year'))
    data = {
        'movies': list(movies.values('title', 'year'))
    }
    return JsonResponse(data)


def single_movie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    data = {
        'movie': {
            'title': movie.title,
            'year': movie.year,
        }
    }
    return JsonResponse(data)


def movie_detail(request, movie_id):
    movie = Movie.objects.filter(pk=movie_id)
    data = {
        'movie':
            list(movie.values('title', 'year'))
    }
    return JsonResponse(data)
