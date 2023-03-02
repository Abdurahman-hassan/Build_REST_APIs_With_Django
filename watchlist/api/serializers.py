"""Serializers for the watchlist app."""
from rest_framework import serializers

from watchlist.models import Movie


# other types of validators
def title_unique(value):
    if Movie.objects.filter(title=value).exists():
        raise serializers.ValidationError('Title must be unique')
    return value


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200, validators=[title_unique]
                                  )  # validators are used to check if the title is unique
    description = serializers.CharField()
    active = serializers.BooleanField(default=False)
    year = serializers.IntegerField()

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # instance.title is the old title
        # validated_data.get('title', instance.title) is the new title
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.year = validated_data.get('year', instance.year)
        instance.save()
        return instance

    # field level validation
    def validate_title(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('Title is too short')
        return value

    # object level validation
    def validate(self, data):
        if data['title'] == data['description']:
            raise serializers.ValidationError('Title and description must be different')
        return data
