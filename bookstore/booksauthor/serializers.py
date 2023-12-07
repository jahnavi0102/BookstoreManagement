from rest_framework import serializers
from .models import Books, Authors


class AuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = ('id', 'name')


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ('title', 'isbn', 'price', 'quantity', 'written_by')

    written_by = AuthorsSerializer(many=True)

    def create(self, validated_data):
        authors_data = validated_data.pop('written_by', [])
        book = Books.objects.create(**validated_data)
        print("ok")
        print(authors_data)
        for author_data in authors_data:
            # Check if author_data is a dictionary, if not, create a dictionary with 'name' key
            if isinstance(author_data, dict):
                author, _ = Authors.objects.get_or_create(**author_data)
            else:
                author, _ = Authors.objects.get_or_create(name=author_data)
            book.written_by.add(author) 
        print("ok1")
        book.save()

        return book


class BooksUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ('quantity', 'price')
