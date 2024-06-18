from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class StreamPlatform(models.Model):
    """A stream platform is a service where movies and TV shows are streamed."""
    name = models.CharField(max_length=30)
    about = models.TextField()
    website = models.URLField()

    def __str__(self):
        return self.name


class WatchList(models.Model):
    """A movie."""
    title = models.CharField(max_length=50)
    storyline = models.TextField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    # each stream platform has many watchlist items
    # and each watchlist item has one stream platform
    platform = models.ForeignKey(StreamPlatform,
                                 on_delete=models.CASCADE,
                                 related_name='watchlist')

    def __str__(self):
        return f"{self.title} ({self.created.year})"


class Review(models.Model):
    """A review for a movie."""
    reviewer = models.ForeignKey(User,
                                 on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),
                                                     MaxValueValidator(5)])
    review = models.CharField(max_length=200, null=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # each review has one movie
    # and each movie has many reviews
    watchlist = models.ForeignKey(WatchList,
                                  on_delete=models.CASCADE,
                                  related_name='reviews')

    def __str__(self):
        return f"{self.watchlist.title} ({self.rating})"
