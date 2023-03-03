from django.db import models




class StreamPlatform(models.Model):
    """A stream platform is a service where movies and TV shows are streamed."""
    name = models.CharField(max_length=200)
    about = models.TextField()
    website = models.URLField()

    def __str__(self):
        return self.name


class WatchMoviesList(models.Model):
    """A movie to watch."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    active = models.BooleanField(default=True)
    year = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.year})"