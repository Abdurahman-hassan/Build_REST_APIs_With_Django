"""Serializers for the watchlist app."""
from rest_framework import serializers

from watchlist.models import WatchMoviesList, StreamPlatform


# we can use ModelSerializer to create a serializer
class MovieSerializer(serializers.ModelSerializer):
    # we can add extra fields to the serializer
    len_title = serializers.SerializerMethodField()

    class Meta:
        model = WatchMoviesList
        # fields = '__all__'
        exclude = ('id', 'date_added',)

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

#
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
