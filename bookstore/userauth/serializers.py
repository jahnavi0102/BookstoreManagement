from rest_framework import serializers
from .models import Users

class UserSerializer(serializers.Serializer):
    class Meta:
        model = Users
        fields = ['email', 'username', 'first_name', 'last_name']

    def create(self, validated_data):
        print(**validated_data)
        return Users.objects.create(**validated_data)

    