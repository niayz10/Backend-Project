from django.shortcuts import render
import logging
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
from base.models import Publisher, Author, Category, Genre, Type
from base.serializers import PublisherSerializer, AuthorSerializer, CategorySerializer, GenreSerializer, TypeSerializer
from rest_framework.generics import get_object_or_404

logger = logging.getLogger(__name__)

class PublisherAPIView(APIView):

    def get(self, request):
        logger.info('list of a users')
        publishers = Publisher.objects.all()
        serializer = PublisherSerializer(publishers, many=True)

        return Response(serializer.data)

    def post(self, request):
        logger.info('creation of a publisher')
        serializer = PublisherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error('error in post method of publisher')
        return Response({'error': serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def select_by_name(self):
        publishers = Publisher.objects.select_by_name()
        serializer = PublisherSerializer(publishers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PublisherDetailAPIView(APIView):
    def get_object(self, publisher_id):
        try:
            return Publisher.objects.get(id=publisher_id)
        except Publisher.DoesNotExist as e:
            logger.error('error does not exist publisher')
            return Response({'error': str(e)})

    def get(self, request, publisher_id):
        logger.info('getting a publisher')
        publisher = self.get_object(publisher_id)
        serializer = PublisherSerializer(publisher)
        return Response(serializer.data)

    def put(self, request, publisher_id):
        logger.info('put method of publisher')
        publisher = self.get_object(publisher_id)
        serializer = PublisherSerializer(instance=publisher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        logger.error('error publisher')
        return Response({'error': serializer.errors})

    def delete(self, request, publisher_id):
        logger.info('publisher delete')
        publisher = self.get_object(publisher_id)
        publisher.delete()
        return Response({'deleted': True})


class AuthorAPIView(APIView):
    def get(self, request):
        logger.info('list of authors')
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

    def post(self, request):
        logger.info('post method of a author')
        serializer = AuthorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error('error post method of a author')
        return Response({'error': serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AuthorDetailAPIView(APIView):
    def get_object(self, id):
        try:
            return Author.objects.get(id=id)
        except Author.DoesNotExist as e:
            logger.error('does not exist author')
            return Response({'error': str(e)})

    def get(self, request, author_id):
        logger.info('getting a author')
        author = self.get_object(author_id)
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

    def put(self, request, author_id):
        logger.info('put method of a author')
        author = self.get_object(author_id)
        serializer = AuthorSerializer(instance=author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        logger.error('error - put method author')
        return Response({'error': serializer.errors})

    def delete(self, request, author_id):
        logger.info('author delete')
        author = self.get_object(author_id)
        author.delete()
        return Response({'deleted': True})


class CategoryViewSet(viewsets.ViewSet):

    def category_list(self, request):
        logger.info('list of categories')
        list = Category.objects.all()
        serializer = CategorySerializer(list, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id):
        logger.info('retrieve a category')
        queryset = Category.objects.all()
        task = get_object_or_404(queryset, id=id)
        serializer = CategorySerializer(task)
        return Response(serializer.data)

    def create(self, request):
        logger.info('creation a category')
        if request.user.role == "Admin":
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, id):
        logger.info('update a category')
        if request.user.role == "Admin":
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CategorySerializer(instance=Category.objects.get(id=id), data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, id):
        logger.info('destroy a category')
        if request.user.role == "Admin":
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        category = Category.objects.get(id=id)
        category.delete()
        return Response({}, status=status.HTTP_200_OK)


class GenreViewSet(viewsets.ViewSet):

    def genre_list(self, request):
        logger.info('list of a genres')
        list = Genre.objects.all()
        serializer = GenreSerializer(list, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id):
        logger.info('retrieve a genre')
        queryset = Genre.objects.all()
        task = get_object_or_404(queryset, id=id)
        serializer = GenreSerializer(task)
        return Response(serializer.data)

    def create(self, request):
        logger.info('creation a genre')
        if request.user.role == "Admin":
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, id):
        logger.info('updating a genre')
        if request.user.role == "Admin":
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        serializer = GenreSerializer(instance=Genre.objects.get(id=id), data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, id):
        logger.info('destroy a genre')
        if request.user.role == "Admin":
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        genre = Genre.objects.get(id=id)
        genre.delete()
        return Response({}, status=status.HTTP_200_OK)


class TypeViewSet(viewsets.ViewSet):

    def type_list(self, request):
        logger.info('list of types')
        list = Type.objects.all()
        serializer = TypeSerializer(list, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id):
        logger.info('retrieve a type')
        queryset = Type.objects.all()
        task = get_object_or_404(queryset, id=id)
        serializer = TypeSerializer(task)
        return Response(serializer.data)

    def create(self, request):
        logger.info('creation a type')
        if request.user.role == "Admin":
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({}, status=status.HTTP_201_CREATED)

    def update(self, request, id):
        logger.info('updating a type')
        if request.user.role == "Admin":
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TypeSerializer(instance=Type.objects.get(id=id), data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, id):
        logger.info('destroy a type')
        if request.user.role == "Admin":
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        type = Type.objects.get(id=id)
        type.delete()
        return Response({}, status=status.HTTP_200_OK)
