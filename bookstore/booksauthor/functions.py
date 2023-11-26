from models import Authors
from serializers import BooksSerializer


def checkAuthor(author):
    if isinstance(author, str):
        author = Authors.objects.get_or_create(name=author)
    else:
        author = Authors.objects.filter(id=author)
    return author


def saveBook(validated_data):
    serializer = BooksSerializer(validated_data)
    if not serializer.is_valid():
        return False, serializer.errors
    serializer.save()
    return True, serializer