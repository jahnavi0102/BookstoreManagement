
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .models import Users
from .functions import usersignup, userlogin
from django.contrib.auth import authenticate, login


class UsersAuth(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """

    def create(self, request):
        """
        Create/Signup user.
        """
        if not request.data.get("email") and not request.data.get("username") and not request.data.get("password"):
            return Response(data = {"Error": "Email, Username and Password fields are mandatory."}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        email = request.data["email"]
        username = request.data["username"]
        password = request.data["password"]
        is_staff = request.data.get("is_staff",False)
        first_name = request.data.get("first_name", None)
        last_name = request.data.get("last_name", None)

        if Users.objects.filter(email=email).exists():
            return Response(data= {"Error": "Signup is already done"}, status=status.HTTP_302_FOUND)
        
        user_data = {
            "email": email,
            "username": username,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "is_staff": is_staff,
            "date_joined":datetime.now()
        }
        statuss, serializer = usersignup(user=user_data)
        if not statuss:
            return Response(data= {"Error": "Fields are not appropriate"}, status=status.HTTP_204_NO_CONTENT)

        result = {"data":user_data, "message": "Created successfully"}
        return Response(data=result, status=status.HTTP_201_CREATED)
    

    def retrieve(self,request):
        """
        Login User and data.get the authentication token.
        """
        if not request.data.get("username") and request.data.get("password"):
            return Response(data = {"Error": "Username and Password fields are mandatory for login."}, status=status.HTTP_406_NOT_ACCEPTABLE)
        username = request.data["username"]
        password = request.data["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            token = userlogin(user=user)
            return Response(data={
                "email": user.email,
                "customer":user.is_staff,
                "access-token": token
            }, status=status.HTTP_200_OK)
        else:
            return Response(data= {"Error": "Either your email is not found or username or password is wrong. Signup or fix the fields"}, status=status.HTTP_302_FOUND)
        

    
    


        








