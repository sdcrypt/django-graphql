import graphene
from graphene_django import DjangoObjectType, DjangoListField
import graphene_django
from api.models import Book

class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = "__all__"

#List Retrieve
class Query(graphene.ObjectType):
    books = graphene.List(BookType)
    book = graphene.Field(BookType, book_id=graphene.Int())

    def resolve_books(self, info, **kwargs):
        return Book.objects.all()
    
    def resolve_book(self, info, book_id):
        return Book.objects.get(pk=book_id)


#We will now add create, update and delete operations through mutations.
class BookInput(graphene.InputObjectType):
    """
    This class defines fields similar to our Book model object to allow the client 
    to add or change the data through the API. We will use this class as an argument for 
    our mutation classes.
    """
    id = graphene.ID()
    title = graphene.String()
    author = graphene.String()
    year_published = graphene.String()
    review = graphene.Int()


class CreateBook(graphene.Mutation):
    """
    Add mutation to create new book
    For every mutation class we must have an Arguments inner class and a mutate() class method.
    """
    class Arguments:
        book_data = BookInput(required=True)
    
    book = graphene.Field(BookType)

    @staticmethod
    def mutate(root, info, book_data=None):
        book_instance = Book(
            title = book_data.title,
            author = book_data.author,
            year_published = book_data.year_published,
            review = book_data.review
        )
        book_instance.save()
        return CreateBook(book=book_instance)

class UpdateBook(graphene.Mutation):
    """
     mutate() method, which retrieves a particular book object 
     from the database by the book ID provided and then applies 
     the changes from the input argument to it.
    """
    class Agruments:
        book_data = BookInput(required=True)
    
    book = graphene.Field(BookType)

    @staticmethod
    def mutate(root, info, book_data=None):
        book_instance = Book.objects.get(pk=book_data.id)

        if book_instance:
            book_instance.title = book_data.title
            book_instance.author = book_data.author
            book_instance.year_published = book_data.year_published
            book_instance.review = book_data.review
            book_instance.save()

            return UpdateBook(book=book_instance)
        return UpdateBook(book=None)
    

class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    book = graphene.Field(BookType)

    @staticmethod
    def mutate(root, info, id):
        book_instance = Book.objects.get(pk=id)
        book_instance.delete()
        return None


class Mutation(graphene.ObjectType):
    """
    class To register these 3 mutations and 2 queries with Graphene
    """
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)