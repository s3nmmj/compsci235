import csv
from bisect import insort_left
from pathlib import Path

from werkzeug.security import generate_password_hash

from library.adapters.jsondatareader import BooksJSONReader
from library.adapters.repository import AbstractRepository
from library.domain.model import Book, Author, User, Publisher, Review, ReadingList


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__users = list()
        self.__books = list()
        self.__books_index = dict()
        self.__authors = list()
        self.__authors_index = dict()
        self.__publishers = set()
        self.__publishers_index = dict()
        self.__author_books_index = dict()
        self.__publisher_books_index = dict()
        self.__release_year_books_index = dict()
        self.__reviews = dict()
        self.__reading_list = dict()

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

    def add_book(self, book: Book):
        insort_left(self.__books, book)
        self.__books_index[book.book_id] = book
        for author in book.authors:
            if self.__author_books_index.get(author.unique_id):
                self.__author_books_index[author.unique_id].append(book)
            else:
                self.__author_books_index[author.unique_id] = [book]
        if book.publisher is not None:
            if self.__publisher_books_index.get(book.publisher.name):
                self.__publisher_books_index[book.publisher.name].append(book)
            else:
                self.__publisher_books_index[book.publisher.name] = [book]

        if book.release_year is not None:
            if self.__release_year_books_index.get(book.release_year):
                self.__release_year_books_index[book.release_year].append(book)
            else:
                self.__release_year_books_index[book.release_year] = [book]

    def get_book(self, book_id: int) -> Book:
        book = None

        try:
            book = self.__books_index[book_id]
        except KeyError:
            pass  # Ignore exception and return None.

        return book

    def get_number_of_books(self) -> int:
        return len(self.__books)

    def get_books_by_indices(self, indices):
        books = [self.__books[index] for index in indices]
        return books

    def get_books(self, offset: int, page_size: int):
        return self.__books[offset * page_size:(offset + 1) * page_size]

    def get_books_by_publisher(self, publisher_name: str):
        books = self.__publisher_books_index.get(publisher_name)
        return books if books else []

    def get_books_by_release_year(self, release_year: int):
        books = self.__release_year_books_index.get(release_year)
        return books if books else []

    def get_books_by_author_id(self, author_id: int):
        books = self.__author_books_index.get(author_id)
        return books if books else []

    def add_author(self, author: Author) -> Author:
        insort_left(self.__authors, author)
        self.__authors_index[author.unique_id] = author
        return author

    def get_author(self, author_id: int) -> Book:
        author = None

        try:
            author = self.__authors_index[author_id]
        except KeyError:
            pass  # Ignore exception and return None.

        return author

    def get_authors(self, offset: int, page_size: int):
        return self.__authors[offset * page_size:(offset + 1) * page_size]

    def get_number_of_authors(self) -> int:
        return len(self.__authors)

    def add_publisher(self, publisher: Publisher) -> Publisher:
        self.__publishers.add(publisher)
        self.__publishers_index[publisher.name] = publisher
        return publisher

    def get_publisher(self, publisher_name: str) -> Book:
        publisher = None

        try:
            publisher = self.__publishers_index[publisher_name]
        except KeyError:
            pass  # Ignore exception and return None.

        return publisher

    def add_review(self, review: Review):
        # call parent class first, add_review relies on implementation of code common to all derived classes
        super().add_review(review)
        book = review.book
        self.__books_index[book.book_id].text_reviews_count += 1
        if self.__reviews.get(book.book_id):
            self.__reviews[book.book_id].append(review)
        else:
            self.__reviews[book.book_id] = [review]

    def get_reviews_by_book_id(self, book_id: int):
        return self.__reviews.get(book_id)

    def add_reading_list(self, reading_list: ReadingList, existing: bool):
        if not existing:
            if self.__reading_list.get(reading_list.user.user_name) is None:
                self.__reading_list[reading_list.user.user_name] = [reading_list]
            else:
                self.__reading_list[reading_list.user.user_name].append(reading_list)

    def get_reading_list_by_user(self, shelf: str, user: User):
        reading_list = []
        reading_lists = self.__reading_list.get(user.user_name)
        if reading_lists is not None:
            for rl in reading_lists:
                if rl.shelf == shelf:
                    reading_list.append(rl)
        return reading_list

    def get_reading_list_by_user_and_book_id(self, user: User, book_id: int) -> ReadingList:
        reading_lists = self.__reading_list.get(user.user_name)
        if reading_lists is None:
            return None
        else:
            reading_list = None
            for rl in reading_lists:
                if rl.book.book_id == book_id:
                    reading_list = rl
                    break

            return reading_list
