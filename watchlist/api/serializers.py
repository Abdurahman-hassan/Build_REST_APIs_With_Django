"""Serializers for the watchlist app."""
from rest_framework import serializers

from watchlist.models import WatchMoviesList, StreamPlatform, Review, Movie


############################################################################################################
# step by step to create a serializer, manually
# I need to convert the 3 simple views that handle
# manually the serialization and deserialization of the data
# to use the serializer class
# movie_list_manual_serializer_deserializer,
# single_movie_manual_serializer_deserializer,
# movie_detail_manual_serializer_deserializer

# serializer level validation
def description_length(value):
    if len(value) < 10:
        raise serializers.ValidationError('Description is too short')


class ManualMovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField(validators=[description_length])
    active = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance



# each Stream has a list of movies -> many movies to one stream
# each movie has one stream -> one stream to many movies
# also each movie has a list of reviews -> many reviews to one movie
# each review has one movie -> one movie to many reviews

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for the review model."""
    reviewer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('watchlist',)


# we can use ModelSerializer to create a serializer
class MovieSerializer(serializers.ModelSerializer):
    # we can add extra fields to the serializer
    len_title = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = WatchMoviesList
        # fields = '__all__'
        exclude = ('date_added',)

    def get_len_title(self, obj):
        return len(obj.title)

    def validate_title(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('Title is too short')

        if WatchMoviesList.objects.filter(title=value).exists():
            raise serializers.ValidationError("Title already exists")

        return value

    # object level validation
    def validate(self, data):
        if data['title'] == data['description']:
            raise serializers.ValidationError('Title and description must be different')
        return data


class StreamPlatformSerializer(serializers.ModelSerializer):
    """Serializer for the stream platform model."""
    # we can use the related_name to get the related objects of watchlist in the stream platform
    watchlist = MovieSerializer(many=True, read_only=True)

    # add string related field to get specific fields of the related objects not all of them
    # watchlist = serializers.StringRelatedField(many=True, read_only=True)
    # add primary key related field to get the primary key of the related objects
    # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # add hyperlink related field to get the url of the related objects
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True, read_only=True, view_name='movie_detail'
    # )
    class Meta:
        model = StreamPlatform
        exclude = ('id',)

    def validateـabout(self, value):
        if len(value) > 500:
            raise serializers.ValidationError('About platform is too long it should be less than 500 characters')
        return value

        # we can use serializers.Serializer to create a serializer
        # other types of validators

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('name is too short')

        if StreamPlatform.objects.filter(name=value).exists():
            raise serializers.ValidationError("name already exists")

        return value

# from drf docs tutorial
# class WatchMoviesList(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(max_length=200, validators=[title_unique]
#                                   )  # validators are used to check if the title is unique
#     description = serializers.CharField()
#     active = serializers.BooleanField(default=False)
#     year = serializers.IntegerField()
#
#     def create(self, validated_data):
#         return WatchMoviesList.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         # instance.title is the old title
#         # validated_data.get('title', instance.title) is the new title
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.year = validated_data.get('year', instance.year)
#         instance.save()
#         return instance
#
#     # field level validation
#     def validate_title(self, value):
#         if len(value) < 2:
#             raise serializers.ValidationError('Title is too short')
#         return value
#
#     # object level validation
#     def validate(self, data):
#         if data['title'] == data['description']:
#             raise serializers.ValidationError('Title and description must be different')
#         return data
