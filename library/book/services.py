from datetime import datetime

from config import Config
from library.adapters.repository import AbstractRepository
from library.domain.model import User, Book, Review, ShelfName, ReadingList

default_page_size = int(Config.BOOKS_PER_PAGE)


class NonExistentBookException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def get_book_by_id(repo: AbstractRepository, book_id):
    return repo.get_book(book_id)


def get_books(repo: AbstractRepository, offset: int = 0):
    return repo.get_books(offset, default_page_size)


def get_books_by_publisher(repo: AbstractRepository, publisher_name: str):
    return repo.get_books_by_publisher(publisher_name)


def get_books_by_release_year(repo: AbstractRepository, release_year: int):
    return repo.get_books_by_release_year(release_year)


def get_books_by_author_id(repo: AbstractRepository, author_id: int):
    return repo.get_books_by_author_id(author_id)


def get_number_of_books(repo: AbstractRepository):
    return repo.get_number_of_books()


def make_review(review_text: str, user: User, book: Book):
    review = Review(user, book, review_text)
    return review


def make_reading_list(shelf: ShelfName, user: User, book: Book, repo: AbstractRepository):
    existing_reading_list = repo.get_reading_list_by_user_and_book_id(user, book.book_id)
    if existing_reading_list is not None:
        existing_reading_list.shelf = shelf
        return existing_reading_list, True
    else:
        reading_list = ReadingList(user, book, shelf)
        return reading_list, False


def get_reviews_by_book_id(repo: AbstractRepository, book_id: int):
    reviews = repo.get_reviews_by_book_id(book_id)
    return reviews


def add_review(book_id: int, review_text: str, user_name: str, repo: AbstractRepository):
    # Check that the book exists.
    book = repo.get_book(book_id)
    if book is None:
        raise NonExistentBookException

    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    # Create review.
    review = make_review(review_text, user, book)

    # Update the repository.
    repo.add_review(review)


def add_book_to_user(user_name: str, book_id: int, shelf_name: str, repo: AbstractRepository):
    # Check that the book exists.
    book = repo.get_book(book_id)
    if book is None:
        raise NonExistentBookException

    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    reading_list, existing = make_reading_list(shelf_name, user, book, repo)
    # Update the repository.
    repo.add_reading_list(reading_list, existing)


def get_books_by_user_and_shelf(repo: AbstractRepository, user_name: str, shelf: ShelfName):
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException
    book_lists = repo.get_reading_list_by_user(shelf.value, user)
    books = [book_list.book for book_list in book_lists]
    return books
