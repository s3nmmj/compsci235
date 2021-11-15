import enum
from datetime import datetime
from typing import List, Iterable


class Publisher:
    def __init__(self, publisher_name: str):
        # This makes sure the setter is called here in the initializer/constructor as well.
        self.name = publisher_name
        self.__books: List[Book] = list()

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, publisher_name: str):
        self.__name = "N/A"
        if isinstance(publisher_name, str):
            # Make sure leading and trailing whitespace is removed.
            publisher_name = publisher_name.strip()
            if publisher_name != "":
                self.__name = publisher_name

    @property
    def books(self) -> Iterable['Book']:
        return iter(self.__books)

    def add_book(self, book: 'Book'):
        self.__books.append(book)

    def __repr__(self):
        return f'<Publisher {self.name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.name == self.name

    def __lt__(self, other):
        return self.name < other.name

    def __hash__(self):
        return hash(self.name)


class Author:

    def __init__(self, author_id: int, author_full_name: str):
        if not isinstance(author_id, int):
            raise ValueError

        if author_id < 0:
            raise ValueError

        self.__unique_id = author_id

        # Uses the attribute setter method.
        self.full_name = author_full_name
        self.__average_rating = 0.0
        self.__text_reviews_count = 0
        self.__ratings_count = 0
        self.__books: List[Book] = list()

    @property
    def unique_id(self) -> int:
        return self.__unique_id

    @property
    def full_name(self) -> str:
        return self.__full_name

    @full_name.setter
    def full_name(self, author_full_name: str):
        if isinstance(author_full_name, str):
            # make sure leading and trailing whitespace is removed
            author_full_name = author_full_name.strip()
            if author_full_name != "":
                self.__full_name = author_full_name
            else:
                raise ValueError
        else:
            raise ValueError

    @property
    def average_rating(self) -> float:
        return self.__average_rating

    @average_rating.setter
    def average_rating(self, average_rating: float):
        if isinstance(average_rating, float):
            self.__average_rating = average_rating
        else:
            raise ValueError

    @property
    def text_reviews_count(self) -> float:
        return self.__text_reviews_count

    @text_reviews_count.setter
    def text_reviews_count(self, text_reviews_count: int):
        if isinstance(text_reviews_count, int):
            self.__text_reviews_count = text_reviews_count
        else:
            raise ValueError

    @property
    def ratings_count(self) -> float:
        return self.__ratings_count

    @ratings_count.setter
    def ratings_count(self, ratings_count: int):
        if isinstance(ratings_count, int):
            self.__ratings_count = ratings_count
        else:
            raise ValueError

    @property
    def books(self) -> Iterable['Article']:
        return iter(self.__books)

    def add_book(self, book: 'Book'):
        self.__books.append(book)

    def __repr__(self):
        return f'<Author {self.full_name}, author id = {self.unique_id}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.unique_id == other.unique_id

    def __lt__(self, other):
        return self.unique_id < other.unique_id

    def __hash__(self):
        return hash(self.unique_id)


class Book:

    def __init__(self, book_id: int, book_title: str):
        if not isinstance(book_id, int):
            raise ValueError

        if book_id < 0:
            raise ValueError

        self.__book_id = book_id

        # use the attribute setter
        self.title = book_title

        self.__description = None
        self.__publisher = None
        self.__authors: List[Author] = list()
        self.__release_year = None
        self.__ebook = None
        self.__num_pages = None

        self.__image_url = None
        self.__isbn = None
        self.__link = None
        self.__ratings_count = None
        self.__average_rating = None
        self.__text_reviews_count = None
        self.__reviews: List[Review] = list()
        self.__reading_lists: List[ReadingList] = list()

    @property
    def book_id(self) -> int:
        return self.__book_id

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, book_title: str):
        if isinstance(book_title, str):
            book_title = book_title.strip()
            if book_title != "":
                self.__title = book_title
            else:
                raise ValueError
        else:
            raise ValueError

    @property
    def release_year(self) -> int:
        return self.__release_year

    @release_year.setter
    def release_year(self, release_year: int):
        if isinstance(release_year, int) and release_year >= 0:
            self.__release_year = release_year
        else:
            raise ValueError

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str):
        if isinstance(description, str):
            self.__description = description.strip()

    @property
    def publisher(self) -> Publisher:
        return self.__publisher

    @publisher.setter
    def publisher(self, publisher: Publisher):
        if isinstance(publisher, Publisher):
            self.__publisher = publisher
        else:
            self.__publisher = None

    @property
    def authors(self) -> List[Author]:
        return self.__authors

    def add_author(self, author: Author):
        if not isinstance(author, Author):
            return

        if author in self.__authors:
            return

        self.__authors.append(author)

    def remove_author(self, author: Author):
        if not isinstance(author, Author):
            return

        if author in self.__authors:
            self.__authors.remove(author)

    @property
    def ebook(self) -> bool:
        return self.__ebook

    @ebook.setter
    def ebook(self, is_ebook: bool):
        if isinstance(is_ebook, bool):
            self.__ebook = is_ebook

    @property
    def num_pages(self) -> int:
        return self.__num_pages

    @num_pages.setter
    def num_pages(self, num_pages: int):
        if isinstance(num_pages, int) and num_pages >= 0:
            self.__num_pages = num_pages

    @property
    def image_url(self) -> str:
        return self.__image_url

    @image_url.setter
    def image_url(self, image_url: bool):
        if isinstance(image_url, str):
            self.__image_url = image_url

    @property
    def isbn(self) -> str:
        return self.__isbn

    @isbn.setter
    def isbn(self, isbn: str):
        if isinstance(isbn, str):
            self.__isbn = isbn

    @property
    def link(self) -> str:
        return self.__link

    @link.setter
    def link(self, link: str):
        if isinstance(link, str):
            self.__link = link

    @property
    def ratings_count(self) -> int:
        return self.__ratings_count

    @ratings_count.setter
    def ratings_count(self, ratings_count: int):
        if isinstance(ratings_count, int):
            self.__ratings_count = ratings_count

    @property
    def average_rating(self) -> float:
        return self.__average_rating

    @average_rating.setter
    def average_rating(self, average_rating: float):
        if isinstance(average_rating, float):
            self.__average_rating = average_rating

    @property
    def text_reviews_count(self) -> int:
        return self.__text_reviews_count

    @text_reviews_count.setter
    def text_reviews_count(self, text_reviews_count: int):
        if isinstance(text_reviews_count, int):
            self.__text_reviews_count = text_reviews_count

    @property
    def reviews(self) -> Iterable['Review']:
        return iter(self.__reviews)

    def add_review(self, review: 'Review'):
        self.__reviews.append(review)

    @property
    def reading_lists(self) -> dict:
        return self.__reading_lists

    def add_reading_list(self, reading_list: 'ReadingList'):
        self.__reading_lists.append(reading_list)

    def __repr__(self):
        return f'<Book {self.title}, book id = {self.book_id}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.book_id == other.book_id

    def __lt__(self, other):
        return self.book_id < other.book_id

    def __hash__(self):
        return hash(self.book_id)


class ShelfName(enum.Enum):
    CURRENTLY_READING = 'Currently Reading'
    WANT_TO_READ = 'Want to Read'
    READ = 'Read'

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value


class User:
    def __init__(self, user_name: str, password: str):
        if user_name == "" or not isinstance(user_name, str):
            self.__user_name = None
        else:
            self.__user_name = user_name.strip()

        if password == "" or not isinstance(password, str) or len(password) < 7:
            self.__password = None
        else:
            self.__password = password

        self.__reading_lists: List[ReadingList] = list()

        self.__reviews: List[Review] = list()

    @property
    def user_name(self) -> str:
        return self.__user_name

    @property
    def password(self) -> str:
        return self.__password

    @property
    def reading_lists(self) -> dict:
        return self.__reading_lists

    def add_reading_list(self, reading_list: 'ReadingList'):
        self.__reading_lists.append(reading_list)

    @property
    def reviews(self) -> Iterable['Review']:
        return iter(self.__reviews)

    def add_review(self, review: 'Review'):
        self.__reviews.append(review)

    def __repr__(self) -> str:
        return f'<User {self.__user_name}>'

    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return other.user_name == self.user_name

    def __lt__(self, other):
        return self.user_name < other.user_name

    def __hash__(self):
        return hash(self.user_name)


class Review:
    def __init__(self, user: User, book: Book, review: str):
        if isinstance(user, User):
            self.__user = user
        else:
            self.__user = None

        if isinstance(book, Book):
            self.__book = book
        else:
            self.__book = None

        if isinstance(review, str):
            self.__review = review.strip()
        else:
            self.__review_text = "N/A"

        self.__timestamp = datetime.now()

    @property
    def user(self) -> User:
        return self.__user

    @property
    def book(self) -> Book:
        return self.__book

    @property
    def review(self) -> str:
        return self.__review

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        return other.user == self.user and other.book == self.book and \
               other.review == self.review and other.timestamp == self.timestamp


class ReadingList:
    def __init__(self, user: User, book: Book, shelf: ShelfName):
        if isinstance(user, User):
            self.__user = user
        else:
            self.__user = None

        if isinstance(book, Book):
            self.__book = book
        else:
            self.__book = None

        self.__shelf = shelf

    @property
    def user(self) -> User:
        return self.__user

    @property
    def book(self) -> Book:
        return self.__book

    @property
    def shelf(self) -> str:
        return self.__shelf

    @shelf.setter
    def shelf(self, shelf: str):
        if isinstance(shelf, str):
            self.__shelf = shelf
