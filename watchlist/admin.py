from django.contrib import admin

# Register your models here.

from .models import WatchMoviesList, StreamPlatform

admin.site.register(WatchMoviesList)
admin.site.register(StreamPlatform)