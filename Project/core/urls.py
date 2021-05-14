from django.urls import path

from core.views import BookViewSet, ComicsViewSet, get_comics_by_category

urlpatterns = [
    path('books', BookViewSet.as_view({'get': 'book_list', 'post': 'create'})),
    path('book/<int:id>', BookViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('book/<int:id>/comments', BookViewSet.as_view({'get': 'comments', 'post': 'write_comment'})),
    path('book/<int:id>/comments/<int:comment_id>', BookViewSet.as_view({'get': 'retrieve_comment',
                                                                         'put': 'modify_comment',
                                                                         'delete': 'destroy_comment'})),
    path('book/<int:id>/rate', BookViewSet.as_view({'put': 'rate'})),
    path('comics', ComicsViewSet.as_view({'get': 'comics_list', 'post': 'create'})),
    path('comics/<int:id>', ComicsViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('comics/<int:id>/comments', ComicsViewSet.as_view({'get': 'comments', 'post': 'write_comment'})),
    path('comics/<int:id>/comments/<int:comment_id>', ComicsViewSet.as_view({'get': 'retrieve_comment',
                                                                             'put': 'modify_comment',
                                                                             'delete': 'destroy_comment'})),
    path('comics/<int:id>/rate', ComicsViewSet.as_view({'put': 'rate'})),
]
