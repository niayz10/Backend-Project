import logging

from django.shortcuts import render
import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
# Create your views here.
from base.models import Mark, Genre, Type, Category
from core.serializers import CommentSerializer, CommentSerializerForComics
from core.models import Book, Comics, Comment, CommentForComics
from core.serializers import BookSerializer, ComicsSerializer

logger = logging.getLogger(__name__)


class BookViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def book_list(self, request):
        logger.info('list of a books')
        list = Book.objects.all()
        serializer = BookSerializer(list, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id):
        logger.info('retrieve a book')
        queryset = Book.objects.all()
        task = get_object_or_404(queryset, id=id)
        serializer = BookSerializer(task)
        return Response(serializer.data)

    def comments(self, request, id):
        logger.info('get comments')
        book = Book.objects.get(id=id)
        try:
            comments = book.comments.all()
        except Comment.DoesNotExist:
            return Response({})
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def write_comment(self, request, id):
        logger.info('post method of a comment')
        if request.user.role == "Admin":
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CommentSerializer(data=request.data,
                                       context={"user": request.user, "journal": Book.objects.get(id=id)})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def modify_comment(self, request, id, comment_id):
        logger.info('updating of comment')
        if request.user.role == "Admin":
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentSerializer(instance=Comment.objects.get(id=comment_id, user=request.user, journal_id=id),
                                       data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy_comment(self, request, id, comment_id):
        logger.info('destroying a comment')
        if request.user.role == "Admin":
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        comment = Comment.objects.filter(id=comment_id, user=request.user, journal_id=id)
        if not comment.exists:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        comment[0].delete()
        return Response({}, status=status.HTTP_200_OK)

    def retrieve_comment(self, request, id, comment_id):
        logger.info('retrieve of a comment')
        queryset = Comment.objects.all()
        task = get_object_or_404(queryset, id=comment_id, user=request.user, journal_id=id)
        serializer = CommentSerializer(task)
        return Response(serializer.data)

    def rate(self, request, id):
        logger.info('rate of a book')
        book = Book.objects.get(id=id)
        book.rating.add_mark(request.user, request.data.get('mark'))
        return Response({'rating'})

    def create(self, request):
        logger.info('post method of a book')
        if request.user.role == "Admin":
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, id):
        logger.info('update of a book')
        if request.user.role == "Admin":
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        serializer = BookSerializer(instance=Book.objects.get(id=id), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, id):
        logger.info('destroy a book')
        if request.user.role == "Admin":
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        book = Book.objects.get(id=id)
        book.delete()
        return Response({}, status=status.HTTP_200_OK)


class ComicsViewSet(viewsets.ViewSet):

    def comics_list(self, request):
        logger.info('list of a comics')
        list = Comics.objects.all()
        serializer = ComicsSerializer(list, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id):
        logger.info('retrieve of a comics')
        queryset = Comics.objects.all()
        task = get_object_or_404(queryset, id=id)
        serializer = ComicsSerializer(task)
        return Response(serializer.data)

    def comments(self, request, id):
        logger.info('get comments')
        book = Comics.objects.get(id=id)
        try:
            comments = book.comments.all()
        except CommentForComics.DoesNotExist:
            return Response({})
        serializer = CommentSerializerForComics(comments, many=True)
        return Response(serializer.data)

    def write_comment(self, request, id):
        logger.info('post method of a comment')
        if request.user.role == "Admin":
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CommentSerializerForComics(data=request.data,
                                       context={"user": request.user, "journal": Comics.objects.get(id=id)})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def modify_comment(self, request, id, comment_id):
        logger.info('updating of comment')
        if request.user.role == "Admin":
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentSerializerForComics(instance=CommentForComics.objects.get(id=comment_id, user=request.user, journal_id=id),
                                       data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy_comment(self, request, id, comment_id):
        logger.info('destroying a comment')
        if request.user.role == "Admin":
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        comment = CommentForComics.objects.filter(id=comment_id, user=request.user, journal_id=id)
        if not comment.exists:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        comment[0].delete()
        return Response({}, status=status.HTTP_200_OK)

    def retrieve_comment(self, request, id, comment_id):
        logger.info('retrieve of a comment')
        queryset = CommentForComics.objects.all()
        task = get_object_or_404(queryset, id=comment_id, user=request.user, journal_id=id)
        serializer = CommentSerializerForComics(task)
        return Response(serializer.data)

    def rate(self, request, id):
        logger.info('rate of a comics')
        comics = Comics.objects.get(id=id)
        comics.rating.add_mark(request.user, request.data.get('mark'))
        return Response({'rating'})

    def create(self, request):
        logger.info('post method of a comics')
        if request.user.role == "Admin":
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ComicsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, id):
        logger.info('updating of comics')
        if request.user.role == "Admin":
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ComicsSerializer(instance=Comics.objects.get(id=id), data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, id):
        logger.info('destroying a comics')
        if request.user.role == "Admin":
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        comics = Comics.objects.get(id=id)
        comics.delete()
        return Response({}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_books_by_genre(request, genre_id):
    logger.info('books by genre')
    try:
        books_by_genre = Book.objects.filter(genre=Genre.objects.get(id=genre_id))
    except Genre.DoesNotExist as e:
        return Response({'error': str(e)})
    if request.method == "GET":
        serializer = BookSerializer(data=books_by_genre, many=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


@api_view(['GET'])
def get_comics_by_genre(request, genre_id):
    logger.info('comics by genre')
    try:
        comics_by_genre = Comics.objects.filter(genre=Genre.objects.get(id=genre_id))
    except Genre.DoesNotExist as e:
        return Response({'error': str(e)})
    if request.method == "GET":
        serializer = ComicsSerializer(data=comics_by_genre, many=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


@api_view(['GET'])
def get_comics_by_type(request, type_id):
    logger.info('comics by type')
    try:
        comics_by_type = Comics.objects.filter(type=Type.objects.get(id=type_id))
    except Type.DoesNotExist as e:
        return Response({'error': str(e)})
    if request.method == "GET":
        serializer = ComicsSerializer(data=comics_by_type, many=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


@api_view(['GET'])
def get_comics_by_category(request, category_id):
    logger.info('comics by category')
    try:
        comics_by_category = Comics.objects.filter(category=Category.objects.get(id=category_id))
    except Category.DoesNotExist as e:
        return Response({'error': str(e)})
    if request.method == "GET":
        serializer = ComicsSerializer(data=comics_by_category, many=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
