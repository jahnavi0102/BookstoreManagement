from django.urls import path

from .views import Books, Author

urlpatterns = [
    path("book-search/<str:name>/", Books.as_view({'get': 'list'}), name="search-book"),
    path("book-lists/", Books.as_view({ 'get': 'list'}), name="lists-book"),
    path("book-details/<int:pk>", Books.as_view({'get': 'retrieve'}), name = "details-book"),
    path("book-create/", Books.as_view({'post': 'create'}), name="create-book"),
    path("book-update/", Books.as_view({'put': 'update'}), name="update-book"),
    path("book-destroy/", Books.as_view({'delete': 'destroy'}), name="delete-book"),
    path("author-lists/", Author.as_view({'get': 'list'}), name="lists-author"),
    path("author-search/<str:name>/", Books.as_view({'get': 'list'}), name="search-author"),
    path("author-details/<int:pk>", Books.as_view({'get': 'retrieve'}), name = "details-book"),
    ]