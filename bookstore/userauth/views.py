
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .models import Users
from .functions import usersignup, userlogin, userUpdate
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication


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
        print(Users.objects.get(username=username))
        if not check_password(Users.objects.get(username=username).password, password):
            return Response(data= {"Error": "username or password is wrong."}, status=status.HTTP_205_RESET_CONTENT)
        user = authenticate(request, username=username)
        if user is not None:
            # login(request, user)
            token = userlogin(user=user)
            return Response(data={
                "email": user.email,
                "customer":user.is_staff,
                "access-token": token
            }, status=status.HTTP_200_OK)
        else:
            return Response(data= {"Error": "Either your email is not found or username or password is wrong. Signup or fix the fields"}, status=status.HTTP_302_FOUND)
        
    
    def update(self, request):
        """
        Update Users password, username, email, first_name, last_name.
        """
        authenticated = [BasicAuthentication]
        permission_classes = [IsAuthenticated]
        data = dict(request.data)
        # user = Users.objects.get(email = request.user.email)
        dicts = {}
        print(data)
        if data.get("new-password") and data.get("old-password"):
            if check_password(data["old-password"], request.user.password):
                dicts["password"] = data["new-password"]
                del data["old-password"]
                del data["new-password"]
            else:
                return Response(data = {"Error": "old-password doesnt matches"}, status=status.HTTP_401_UNAUTHORIZED)
        
        elif not data and (not data.get("new-password") or not data.get("old-password")):
            return Response(data = {"Error": "old-password and new-password required to update password"}, status=status.HTTP_206_PARTIAL_CONTENT)

        statuss, serializer = userUpdate(user=request.user, data=data)
        if not statuss:
            return Response(data= {"Error": "Only (username, email, old-password, new-password, first_name, last_name allowed.)"}, status=status.HTTP_204_NO_CONTENT)

        return Response(data=f"User updated successfully {request.user.username}", status=status.HTTP_201_CREATED)
        



    
        

    
    


        








