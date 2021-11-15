import pytest

from library.domain.model import User, Book, Publisher, Author, Review


def test_repository_can_add_a_user(in_memory_repo):
    user = User('dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_book_count(in_memory_repo):
    number_of_books = in_memory_repo.get_number_of_books()

    # Check that the query returned 6 Articles.
    assert number_of_books == 3


def test_repository_can_add_book(in_memory_repo):
    book = Book(874658, "Harry Potter")
    in_memory_repo.add_book(book)

    assert in_memory_repo.get_book(book.book_id) == book


def test_repository_can_retrive_a_book(in_memory_repo):
    book = Book(874658, "Harry Potter")
    in_memory_repo.add_book(book)
    book1 = in_memory_repo.get_book(874658)
    assert book1 is book


def test_repository_can_retrive_a_non_existent_book(in_memory_repo):
    book1 = in_memory_repo.get_book(1234)
    assert book1 is None


def test_repository_can_get_books_by_indices(in_memory_repo):
    book1 = Book(874658, "Harry Potter")
    book2 = Book(874659, "Harry Potter 1")
    in_memory_repo.add_book(book1)
    in_memory_repo.add_book(book2)

    books = in_memory_repo.get_books_by_indices([0, 1])

    assert books[0] is book1
    assert books[1] is book2


def test_repository_can_get_books(in_memory_repo):
    book1 = Book(874658, "Harry Potter")
    book2 = Book(874659, "Harry Potter 1")
    in_memory_repo.add_book(book1)
    in_memory_repo.add_book(book2)

    books = in_memory_repo.get_books(0, 2)

    assert books[0] is book1
    assert books[1] is book2


def test_repository_can_get_books_by_publisher(in_memory_repo):
    book1 = Book(874658, "Harry Potter")
    book2 = Book(874659, "Harry Potter 1")
    publisher = Publisher("test")
    book1.publisher = publisher
    book2.publisher = publisher
    in_memory_repo.add_book(book1)
    in_memory_repo.add_book(book2)

    books = in_memory_repo.get_books_by_publisher(publisher.name)
    assert len(books) is 2
    assert books[0] is book1
    assert books[1] is book2


def test_repository_can_get_books_by_release(in_memory_repo):
    book1 = Book(874658, "Harry Potter")
    book2 = Book(874659, "Harry Potter 1")

    book1.release_year = 2021
    book2.release_year = 2020
    in_memory_repo.add_book(book1)
    in_memory_repo.add_book(book2)

    books = in_memory_repo.get_books_by_release_year(2021)

    assert len(books) is 1
    assert books[0] is book1


def test_repository_can_get_books_author_id(in_memory_repo):
    book1 = Book(874658, "Harry Potter")
    book2 = Book(874659, "Harry Potter 1")
    author = Author(123, 'test author')
    book1.add_author(author)
    book2.add_author(author)
    in_memory_repo.add_book(book1)
    in_memory_repo.add_book(book2)

    books = in_memory_repo.get_books_by_author_id(123)

    assert len(books) is 2
    assert books[0] is book1
    assert books[1] is book2


def test_repository_can_add_author(in_memory_repo):
    author = Author(123, 'test author')
    in_memory_repo.add_author(author)

    assert in_memory_repo.get_author(123) is author


def test_repository_can_retrieve_an_author(in_memory_repo):
    author = Author(123, 'test author')
    in_memory_repo.add_author(author)

    author1 = in_memory_repo.get_author(123)
    assert author1 is author


def test_repository_can_retrive_a_non_existent_author(in_memory_repo):
    author = in_memory_repo.get_author(123)
    assert author is None


def test_repository_can_get_authors(in_memory_repo):
    author1 = Author(123, 'test author 1')
    in_memory_repo.add_author(author1)
    author2 = Author(124, 'test author 2')
    in_memory_repo.add_author(author2)

    authors = in_memory_repo.get_authors(0, 2)
    assert len(authors) is 2
    assert authors[0] is author1
    assert authors[1] is author2


def test_repository_can_get_authors_number(in_memory_repo):
    authors_number = in_memory_repo.get_number_of_authors()
    assert authors_number is 5


def test_repository_can_add_publisher(in_memory_repo):
    publisher = Publisher('test publisher')
    in_memory_repo.add_publisher(publisher)
    assert in_memory_repo.get_publisher(publisher.name) is publisher


def test_repository_can_add_review(in_memory_repo):
    user = User('dave', '123456789')
    in_memory_repo.add_user(user)
    book = Book(874658, "Harry Potter")
    book.text_reviews_count = 0
    in_memory_repo.add_book(book)
    review = Review(user, book, 'test review')
    in_memory_repo.add_review(review)

    reviews = in_memory_repo.get_reviews_by_book_id(book.book_id)
    assert len(reviews) is 1
    assert reviews[0] is review
    assert book.text_reviews_count is 1
