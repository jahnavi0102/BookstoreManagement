from rest_framework import serializers
from .models import Books, Authors


class AuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = ('id', 'name', 'books')

    books = serializers.StringRelatedField(many=True)



class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ('title', 'isbn', 'price', 'quantity', 'written_by')

    written_by = AuthorsSerializer(many=True)

    def create(self, validated_data):
        book = Books.objects.create(**validated_data)
        book.save()
        return book





    