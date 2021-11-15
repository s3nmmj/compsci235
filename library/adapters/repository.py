import abc

from library.domain.model import User, Book, Author, Publisher, Review, ReadingList

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        """ Returns the User named user_name from the repository.

        If there is no User with the given user_name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_book(self, book: Book):
        """ Adds a Book to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_book(self, book_id: int) -> Book:
        """ Returns Book with book_id from the repository.

        If there is no Book with the given book_id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_indices(self, indices):
        """ Returns a list of Book, whose ids match those in id_list, from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_books(self, offset: int, page_size: int):
        """ Returns all Books.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_publisher(self, publisher_name: str):
        """ Returns a list of Book, whose publisher name match the given publisher_name, from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_release_year(self, release_year: int):
        """ Returns a list of Book, whose release year match the given release_year, from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_books_by_author_id(self, author_id: int):
        """ Returns a list of Book, whose author id match the given author_id, from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_books(self) -> int:
        """ Returns the number of Books in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_author(self, author: Author) -> Author:
        """ Adds an Author to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_author(self, author_id: int) -> Book:
        """ Returns Author with author_id from the repository.

        If there is no Author with the given author_id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_authors(self, offset: int, page_size: int):
        """ Returns all Author.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_authors(self) -> int:
        """ Returns the number of Authors in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_publisher(self, publisher: Publisher) -> Publisher:
        """ Adds a Publisher to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_publisher(self, publisher_name: str) -> Book:
        """ Returns Author with publisher_name from the repository.

        If there is no Publisher with the given publisher_name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a Review to the repository.

        If the Review doesn't have bidirectional links with a Book and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """

        if review.book is None:
            raise RepositoryException('Review not correctly attached to a Book')

    @abc.abstractmethod
    def get_reviews_by_book_id(self, book_id: int):
        """ Returns the Reviews stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_reading_list(self, reading_list: ReadingList, existing: bool):
        """ Adds a ReadingList to the repository.

        If the ReadingList doesn't have bidirectional links with a Book and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """

        if ReadingList.book is None:
            raise RepositoryException('Review not correctly attached to a Book')

    @abc.abstractmethod
    def get_reading_list_by_user(self, shelf: str, user: User):
        """ Returns the ReadingList stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_reading_list_by_user_and_book_id(self, user: User, book_id: int) -> ReadingList:
        """ Returns the ReadingList stored in the repository. """
        raise NotImplementedError
