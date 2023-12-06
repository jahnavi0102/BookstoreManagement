from .models import Authors
from .serializers import BooksSerializer


def checkAuthor(authors):
    author_list = []
    if isinstance(authors, list):
        for author in authors:
            if type(author) == str:
                author, created = Authors.objects.get_or_create(name=author)
                print(author.name)
                author_list.append({"id":author.id, "name":author.name})
            else:
                print("ok")
                author_list.append({"id":author.id, "name":Authors.objects.filter(id=author).name})

    print(author_list)
    return author_list


def saveBook(validated_data):
    serializer = BooksSerializer(data=validated_data)
    if not serializer.is_valid():
        return serializer.errors, False
    serializer.save()
    print(serializer)
    return serializer, True