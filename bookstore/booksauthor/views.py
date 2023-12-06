from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import BooksSerializer, AuthorsSerializer
from .models import Books, Authors
from .functions import checkAuthor, saveBook


class Books(viewsets.ViewSet):
    """
    Book viewset demonstrating the standard
    actions that will be handled by a router class.
    """
    def list(self, request, name=None):

        authenticated = [BasicAuthentication]
        permission_classes = [IsAuthenticated]

        if name:
            books = Books.objects.filter(title__icontains=name, quantity__gt=0)
        else:
            books = Books.objects.filter( quantity__gt=0)
        if not books:
            return Response(data={"Error":"No books in the store currently"}, status=status.HTTP_200_OK)
        
        serializer = BooksSerializer(books, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    
    def retrieve(self, request, pk=None):
        pass

    def create(self, request):

        authenticated = [BasicAuthentication]
        permission_classes = [IsAuthenticated and IsAdminUser]

        if not (request.data.get("title") or request.data.get("isbn") or request.data.get("price") or request.data.get("quantity") or request.data.get("written_by")):
            return Response(data={"Error": "'title', 'isbn', 'price', 'quantity', 'written_by' is required"})
        
        written_by = request.data["written_by"].split(",")
        written = []
        for author in written_by:
            written_by.append({"name":author})
        print(written)
        
        
        dicts = {}

        dicts["title"] = request.data.get("title")
        dicts["isbn"] = request.data.get("isbn")
        dicts["price"] = request.data.get("price")
        dicts["quantity"] = request.data.get("quantity")
        dicts["written_by"] = written

        serializer, statuss = saveBook(validated_data=dicts)
        print(serializer, statuss)

        if not statuss:
            return Response(data= {"Error": serializer}, status=status.HTTP_204_NO_CONTENT)

        result = {"message": "Created successfully"}
        return Response(data=result, status=status.HTTP_201_CREATED)


    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

class Author(viewsets.ViewSet):
    """
    Author viewset demonstrating the standard
    actions that will be handled by a router class.
    """
    def list(self, request, name=None):
        pass

    def retrieve(self, request, pk=None):
        pass

        