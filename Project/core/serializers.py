from rest_framework import serializers

from auth_.models import CustomUser
from auth_.serializers import CustomUserSerializerForComment
from base.models import Genre, Publisher, Author, Type, Category
from base.serializers import JournalBaseSerializer, TypeSerializer, CategorySerializer
from core.models import Book, Comics, Comment, CommentForComics


class BookSerializer(JournalBaseSerializer):
    id = serializers.IntegerField(read_only=True)
    num_pages = serializers.IntegerField(default=0)

    def create(self, validated_data):
        genre_id = validated_data.get('genre_id')
        validated_data.pop('genre_id')
        validated_data.setdefault('author', Author.objects.get(id=validated_data.get('author_id')))
        validated_data.setdefault('publisher', Publisher.objects.get(id=validated_data.get('publisher_id')))
        validated_data.setdefault('file', validated_data.get('file'))
        book = Book.objects.create(**validated_data)
        for id in genre_id:
            g = Genre.objects.get(id=id)
            book.genre.add(g)
        book.save()
        return book

    def update(self, instance, validated_data):
        genre_id = validated_data.get('genre_id')
        # validated_data.pop('genre_id')
        instance.genre.set(Genre.objects.filter(id__in=genre_id))
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.publication_date = validated_data.get('publication_date', instance.publication_date)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.author = validated_data.get('author', instance.author)
        instance.publisher = validated_data.get('publisher', instance.publisher)
        instance.num_pages = validated_data.get('num_pages', instance.num_pages)
        instance.file = validated_data.get('file', instance.file)
        instance.save()
        return instance

    def validate_num_pages(self, value):
        if value < 0:
            raise ValueError("Number of pages must be positive!!!")
        return value


class ComicsSerializer(JournalBaseSerializer):
    id = serializers.IntegerField(read_only=True)
    type = TypeSerializer(read_only=True, many=True)
    type_id = serializers.ListField(write_only=True)
    category = CategorySerializer(read_only=True, many=True)
    category_id = serializers.ListField(write_only=True)
    num_of_chapters = serializers.IntegerField(default=0)

    def validate_num_of_chapters(self, value):
        if value < 0:
            raise serializers.ValidationError("Number of pages must be positive!!!")
        return value

    def create(self, validated_data):
        print("create method")
        genre_id = validated_data.get('genre_id')
        validated_data.pop('genre_id')
        type_id = validated_data.get('type_id')
        validated_data.pop('type_id')
        category_id = validated_data.get('category_id')
        validated_data.pop('category_id')
        validated_data.setdefault('author', Author.objects.get(id=validated_data.get('author_id')))
        validated_data.setdefault('publisher', Publisher.objects.get(id=validated_data.get('publisher_id')))
        comics = Comics.objects.create(**validated_data)
        # for id in genre_id:
        #     g = Genre.objects.get(id=id)
        #     comics.genre.add(g)
        objects = Genre.objects.filter(id__in=genre_id)
        comics.genre.set(Genre.objects.filter(id__in=genre_id))
        comics.type.set(Type.objects.filter(id__in=type_id))
        comics.category.set(Category.objects.filter(id__in=category_id))
        comics.save()
        return comics

    def update(self, instance, validated_data):
        genre_id = validated_data.get('genre_id')
        validated_data.pop('genre_id')
        type_id = validated_data.get('type_id')
        validated_data.pop('type_id')
        category_id = validated_data.get('category_id')
        validated_data.pop('category_id')
        instance.genre.set(Genre.objects.filter(id__in=genre_id))
        instance.type.set(Type.objects.filter(id__in=type_id))
        instance.category.set(Category.objects.filter(id__in=category_id))
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.publication_date = validated_data.get('publication_date', instance.publication_date)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.author = validated_data.get('author', instance.author)
        instance.publisher = validated_data.get('publisher', instance.publisher)
        instance.num_of_chapters = validated_data.get('num_of_chapters', instance.num_of_chapters)
        instance.save()
        return instance


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    date = serializers.DateField(read_only=True)
    content = serializers.CharField(max_length=1000)
    user = CustomUserSerializerForComment(read_only=True)

    def create(self, validated_data):
        validated_data.setdefault('user', self.context.get('user'))
        validated_data.setdefault('journal', self.context.get('journal'))
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance


class CommentSerializerForComics(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    date = serializers.DateField(read_only=True)
    content = serializers.CharField(max_length=1000)
    user = CustomUserSerializerForComment(read_only=True)

    def create(self, validated_data):
        validated_data.setdefault('user', self.context.get('user'))
        validated_data.setdefault('journal', self.context.get('journal'))
        return CommentForComics.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
