
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .models import Users
from .functions import usersignup, userlogin, userUpdate
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, TokenAuthentication


class UsersAuth(viewsets.ViewSet):
    """
    Viewset demonstrating the standard
    actions that will be handled by a router class.
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
            return Response(data= {"Error": "Signup is already done, or email already exists."}, status=status.HTTP_302_FOUND)
        
        if Users.objects.filter(username=username).exists():
            return Response(data= {"Error": "Username already exists."}, status=status.HTTP_302_FOUND)

        
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

        user = authenticate(request, username=username, password=password, is_active=True)

        if user is not None:
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
        self.authentication_classes = [TokenAuthentication]
        self.permission_classes = [IsAuthenticated]

        data = {}
        update_password = False

        if not request.user.is_authenticated:
            return Response(data = {"Message": "Authentication failed."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not request.user.is_active:
            return Response(data = {"Message": "No user exist."}, status=status.HTTP_400_BAD_REQUEST)

        if not request.data:
            return Response(data = {"Message": "No value to update."},status=status.HTTP_400_BAD_REQUEST)
        
        if (request.data.get("new_password") and not request.data.get("old_password")) or (not request.data.get("new_password") and request.data.get("old_password")):
            return Response(data = {"Error": "old-password and new-password required to update password"}, status=status.HTTP_206_PARTIAL_CONTENT)
        else:
            if request.data.get("first_name"):
                data["first_name"] = request.data["first_name"]
            if request.data.get("last_name"):
                data["last_name"] = request.data["last_name"]
            if request.data.get("email"):
                if Users.objects.filter(username=request.data["username"]):
                    return Response(data={"Error": "Username already exists insert a new username"}, status=status.HTTP_205_RESET_CONTENT)
                data["email"] = request.data["email"]
            if request.data.get("username"):
                if Users.objects.filter(username=request.data["username"]):
                    return Response(data={"Error": "Username already exists insert a new username"}, status=status.HTTP_205_RESET_CONTENT)
                data["username"] = request.data["username"]
            if request.data.get("new_password"):
                update_password = True
                data["password"] = request.data["new_password"]
            if request.data.get("old_password"):
                data["old_password"] = request.data["old_password"]

        if request.data and not data:
            return Response(data = {"Error": "Wrong value to update"}, status=status.HTTP_205_RESET_CONTENT)
        
        if update_password:
            if data.get("new-password") and data.get("old-password"):
                if check_password(data["old-password"], request.user.password):
                    del data["old-password"]
                else:
                    return Response(data = {"Error": "old-password doesnt matches"}, status=status.HTTP_401_UNAUTHORIZED)
            
        statuss, serializer = userUpdate(user=request.user, data=data)

        if not statuss:
            return Response(data= {"Error": serializer}, status=status.HTTP_204_NO_CONTENT)
        
        return Response(data=f"User updated successfully {request.user.username}", status=status.HTTP_201_CREATED)
    

    def destroy(self, request):
        """
        Update Users password, username, email, first_name, last_name.
        """
        authenticated = [BasicAuthentication]
        permission_classes = [IsAuthenticated]

        if not request.user.is_active:
            return Response(data = {"Message": "No user exist."}, status=status.HTTP_400_BAD_REQUEST)

        if not request.data.get("username") or not request.data.get("password"):
            return Response(data = {"Error": "Username and Password fields are mandatory."}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        if request.user.username == request.data["username"]:
            statuss, serializer = userUpdate(user=request.user, data={"is_active":False})
            if not statuss:
                return Response(data= {"Error": serializer}, status=status.HTTP_204_NO_CONTENT)
            
        else:
            return Response(data = {"Error": "Wrong username"}, status=status.HTTP_205_RESET_CONTENT)
        
        return Response(data={"Message": "Deleted successfully"}, status=status.HTTP_200_OK)



        
        



    
        

    
    


        








