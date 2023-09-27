from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from .models import Users

def signup(user:Users):
    serializer = UserSerializer(data=user)
    return serializer

def login(user:Users):
    token,created = Token.objects.get_or_create(user=user)
    return token.key
    