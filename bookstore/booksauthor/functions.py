from .models import Authors
from .serializers import BooksSerializer


def getAuthorDict(authors):
    author_list = []
    for author in authors:
            author_list.append({"name":author})
    return author_list


def saveBook(validated_data):
    serializer = BooksSerializer(data=validated_data)
    if not serializer.is_valid():
        return serializer.errors, False
    serializer.save()
    return serializer, True

