from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Users
from .functions import usersignup, userlogin
from django.contrib.auth import authenticate, login
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

# Create your views here.

class BooksAuthor(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    def create(self, request):
        permission_classes = [IsAuthenticated]
        