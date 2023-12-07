from django.urls import path

from .views import BooksViewSet, Author

urlpatterns = [
    path("book-search/<str:name>/", BooksViewSet.as_view({'get': 'list'}), name="search-book"),
    path("book-lists/", BooksViewSet.as_view({ 'get': 'list'}), name="lists-book"),
    path("book-details/<int:pk>", BooksViewSet.as_view({'get': 'retrieve'}), name = "details-book"),
    path("book-create/", BooksViewSet.as_view({'post': 'create'}), name="create-book"),
    path("book-update/", BooksViewSet.as_view({'put': 'update'}), name="update-book"),
    path("book-destroy/", BooksViewSet.as_view({'delete': 'destroy'}), name="delete-book"),
    path("author-lists/", Author.as_view({'get': 'list'}), name="lists-author"),
    path("author-search/<str:name>/", BooksViewSet.as_view({'get': 'list'}), name="search-author"),
    path("author-details/<int:pk>", BooksViewSet.as_view({'get': 'retrieve'}), name = "details-book"),
    ]