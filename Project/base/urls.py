from django.urls import path

from base.views import PublisherAPIView, PublisherDetailAPIView, AuthorAPIView, AuthorDetailAPIView, CategoryViewSet, \
    GenreViewSet, TypeViewSet, select_by_name
from core.views import get_comics_by_category, get_comics_by_genre, get_books_by_genre, get_comics_by_type

urlpatterns = [
    path('publishers', PublisherAPIView.as_view()),
    path('publishers/by_name', select_by_name),
    path('publisher/<int:publisher_id>', PublisherDetailAPIView.as_view()),
    path('authors', AuthorAPIView.as_view()),
    path('author/<int:author_id>', AuthorDetailAPIView.as_view()),
    path('categories', CategoryViewSet.as_view({'get': 'category_list', 'post': 'create'})),
    path('category/<int:id>', CategoryViewSet.as_view({'put': 'update', 'delete': 'destroy', 'get': 'retrieve'})),
    path('category/<int:category_id>/comics', get_comics_by_category),
    path('genres', GenreViewSet.as_view({'get': 'genre_list', 'post': 'create'})),
    path('genre/<int:id>', GenreViewSet.as_view({'put': 'update', 'delete': 'destroy', 'get': 'retrieve'})),
    path('genre/<int:genre_id>/comics', get_comics_by_genre),
    path('genre/<int:genre_id>/books', get_books_by_genre),
    path('types', TypeViewSet.as_view({'get': 'type_list', 'post': 'create'})),
    path('type/<int:id>', TypeViewSet.as_view({'put': 'update', 'delete': 'destroy', 'get': 'retrieve'})),
    path('type/<int:type_id>/comics', get_comics_by_type),

]
