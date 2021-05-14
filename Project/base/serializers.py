from django.core.validators import MaxLengthValidator
from rest_framework import serializers

from auth_.serializers import CustomUserSerializerForComment
from base.models import Publisher, Author, Category, Genre, Type, Rating, JournalBase
from utils.constants import cities, countries


class PublisherSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=400)
    website = serializers.CharField(max_length=300)
    city = serializers.CharField(max_length=255)
    country = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return Publisher.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.website = validated_data.get('website', instance.website)
        instance.city = validated_data.get('city', instance.city)
        instance.country = validated_data.get('country', instance.country)
        instance.save()
        return instance

    def validate_city(self, value):
        for city in cities:
            if value == city:
                return value
        raise serializers.ValidationError("No such city in the list of validation")

    def validate_countries(self, value):
        for country in countries:
            if value == country:
                return value
        raise serializers.ValidationError("No such country in the list of validation")

    def validate_website(self, value):
        if value == '@^(http\:\/\/|https\:\/\/)?([a-z0-9][a-z0-9\-]*\.)+[a-z0-9][a-z0-9\-]*$@i':
            return value
        raise serializers.ValidationError("Not correct input")



class AuthorSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()

    def validate_first_name(self, value):
        if '/^[a-z0-9_-]{3,16}$/' in value:
            raise serializers.ValidationError("invalid chars in name")
        return value

    def validate_last_name(self, value):
        if '/^[a-z0-9_-]{3,16}$/' in value:
            raise serializers.ValidationError("invalid chars in surname")
        return value

    def validate_email(self, email):
        if email == '/^[A-Z0-9._%+-]+@[A-Z0-9-]+.+.[A-Z]{2,4}$/i':
            return email
        raise serializers.ValidationError("The email is not entered correctly")

    def create(self, validated_data):
        return Author.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


class RatingSerializer(serializers.Serializer):
    average = serializers.ReadOnlyField()
    count = serializers.ReadOnlyField()


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=1000, required=False, validators=[MaxLengthValidator(1000)])

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class GenreSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=1000, required=False, validators=[MaxLengthValidator(1000)])

    def create(self, validated_data):
        return Genre.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

    def validate_name(self, value):
        if '_' in value:
            raise serializers.ValidationError('invalid chars in title')
        return value


class TypeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=1000)

    def create(self, validated_data):
        return Type.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

    def validate_name(self, value):
        if '_' in value:
            raise serializers.ValidationError('invalid chars in title')
        return value


class JournalBaseSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=1000)
    publication_date = serializers.DateField(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    genre_id = serializers.ListField(write_only=True)
    rating = RatingSerializer(read_only=True)
    author = AuthorSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True)
    publisher = PublisherSerializer(read_only=True)
    publisher_id = serializers.IntegerField(write_only=True)

    def validate_title(self, value):
        if '_' in value:
            raise serializers.ValidationError('invalid chars in title')
        return value

    def create(self):
        pass

    def update(self):
        pass
