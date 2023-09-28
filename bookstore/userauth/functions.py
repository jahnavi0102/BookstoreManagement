from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from .models import Users

def usersignup(user:Users):
    serializer = UserSerializer(data=user)

    if not serializer.is_valid():
        return False, serializer.errors
    serializer.save()
    return True, serializer

def userlogin(user:Users):
    token,created = Token.objects.get_or_create(user=user)
    return token.key
    