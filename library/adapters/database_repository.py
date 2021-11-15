from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import scoped_session

from library.adapters.repository import AbstractRepository
from flask import _app_ctx_stack

from library.domain.model import Review, Book, Publisher, Author, User, ReadingList


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def add_book(self, book: Book):
        with self._session_cm as scm:
            scm.session.add(book)
            scm.commit()

    def get_book(self, book_id: int) -> Book:
        book = None
        try:
            book = self._session_cm.session.query(Book).filter(Book._Book__book_id == book_id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return book

    def get_books_by_indices(self, indices):
        books = self._session_cm.session.query(Book).order_by(Book._Book__book_id).all()
        result = list()
        for index in indices:
            if index < len(books):
                result.append(books[index])
        return result

    def get_books(self, offset: int, page_size: int):
        books = self._session_cm.session.query(Book).order_by(Book._Book__book_id).limit(page_size).offset(offset).all()
        return books

    def get_books_by_publisher(self, publisher_name: str):
        books = self._session_cm.session.query(Book).filter(Book.publisher_name == publisher_name).all()
        return books

    def get_books_by_release_year(self, release_year: int):
        books = self._session_cm.session.query(Book).filter(Book._Book__release_year == release_year).all()
        return books

    def get_books_by_author_id(self, author_id: int):
        book_ids = self._session_cm.session.execute('SELECT book_id FROM book_authors WHERE author_id = :author_id',
                                                    {'author_id': author_id}).fetchall()
        book_ids = [id[0] for id in book_ids]

        books = self._session_cm.session.query(Book).filter(Book._Book__book_id.in_(book_ids)).all()
        return books

    def get_number_of_books(self) -> int:
        count = self._session_cm.session.query(Book).count()
        return count

    def add_author(self, author: Author) -> Author:
        existing_author = self.get_author(author.unique_id)
        if existing_author is None:
            with self._session_cm as scm:
                scm.session.merge(author)
                scm.commit()
            return author
        else:
            return existing_author

    def get_author(self, author_id: int) -> Book:
        author = None
        try:
            author = self._session_cm.session.query(Author).filter(
                Author._Author__unique_id == author_id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return author

    def get_authors(self, offset: int, page_size: int):
        authors = self._session_cm.session.query(Author).order_by(Author._Author__unique_id).limit(page_size).offset(
            offset).all()
        return authors

    def get_number_of_authors(self) -> int:
        count = self._session_cm.session.query(Author).count()
        return count

    def add_publisher(self, publisher: Publisher):
        existing_publisher = self.get_publisher(publisher.name)
        if existing_publisher is None:
            with self._session_cm as scm:
                scm.session.add(publisher)
                scm.commit()
            return publisher
        else:
            return existing_publisher

    def get_publisher(self, publisher_name: str) -> Book:
        publisher = None
        try:
            publisher = self._session_cm.session.query(Publisher).filter(
                Publisher._Publisher__name == publisher_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return publisher

    def add_review(self, review: Review):
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_reviews_by_book_id(self, book_id: int):
        reviews = []
        try:
            reviews = self._session_cm.session.query(Review).filter(Review.book_id == book_id).all()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return reviews

    def add_reading_list(self, reading_list: ReadingList, existing: bool):
        with self._session_cm as scm:
            scm.session.add(reading_list)
            scm.commit()

    def get_reading_list_by_user(self, shelf: str, user: User):
        reading_lists = []
        try:
            reading_lists = self._session_cm.session.query(ReadingList).filter(
                and_(ReadingList.user_id == user.id, ReadingList._ReadingList__shelf == shelf)).all()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return reading_lists

    def get_reading_list_by_user_and_book_id(self, user: User, book_id: int) -> ReadingList:
        reading_list = []
        try:
            reading_list = self._session_cm.session.query(ReadingList).filter(
                and_(ReadingList.user_id == user.id, ReadingList.book_id == book_id)).all()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return reading_list[0] if len(reading_list) > 0 else None
