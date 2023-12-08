from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import BooksSerializer, AuthorsSerializer

from .models import Books, Authors
from .functions import getAuthorDict, saveBook



class BooksViewSet(viewsets.ViewSet):
    """
    Book viewset demonstrating the standard
    actions that will be handled by a router class.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def list(self, request, name=None):

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

        self.check_permissions = [IsAdminUser]

        if not all(request.data.get(field) for field in ["title", "isbn", "price", "quantity", "written_by"]):
            return Response(data={"Error": "'title', 'isbn', 'price', 'quantity', 'written_by' is required"})
        
        written_by = request.data["written_by"].split(",")
        written = getAuthorDict(written_by)

        dicts = {
            "title": request.data.get("title"),
            "isbn": request.data.get("isbn"),
            "price": request.data.get("price"),
            "quantity": request.data.get("quantity"),
            "written_by": written
        }

        serializer, statuss = saveBook(validated_data=dicts)

        if not statuss:
            return Response(data= {"Error": serializer}, status=status.HTTP_204_NO_CONTENT)

        return Response(data={"message": "Created successfully"}, status=status.HTTP_201_CREATED)


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

        