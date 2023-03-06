from django.contrib import admin

# Register your models here.

from .models import WatchMoviesList, StreamPlatform, Review

admin.site.register(WatchMoviesList)
admin.site.register(StreamPlatform)
admin.site.register(Review)