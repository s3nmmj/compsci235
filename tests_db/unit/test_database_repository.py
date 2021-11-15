from library.adapters.database_repository import SqlAlchemyRepository
from library.domain.model import User, Book, Publisher, Author, Review


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('dave', '123456789')
    repo.add_user(user)
    user1 = repo.get_user('dave')
    assert user1 == user and user1 is user


def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_book_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    number_of_books = repo.get_number_of_books()

    # Check that the query returned 6 Articles.
    assert number_of_books == 3


def test_repository_can_add_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book = Book(874658, "Harry Potter")
    repo.add_book(book)

    assert repo.get_book(book.book_id) == book


def test_repository_can_retrive_a_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book = Book(874658, "Harry Potter")
    repo.add_book(book)
    book1 = repo.get_book(874658)
    assert book1 is book


def test_repository_can_retrive_a_non_existent_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book1 = repo.get_book(1234)
    assert book1 is None


def test_repository_can_get_books_by_indices(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book1 = Book(874658, "Harry Potter")
    book2 = Book(874659, "Harry Potter 1")
    repo.add_book(book1)
    repo.add_book(book2)

    books = repo.get_books_by_indices([0, 1])

    assert books[0] is book1
    assert books[1] is book2


def test_repository_can_get_books(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book1 = Book(874658, "Harry Potter")
    book2 = Book(874659, "Harry Potter 1")
    repo.add_book(book1)
    repo.add_book(book2)

    books = repo.get_books(0, 2)

    assert books[0] is book1
    assert books[1] is book2


def test_repository_can_get_books_by_publisher(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book1 = Book(874658, "Harry Potter")
    book2 = Book(874659, "Harry Potter 1")
    publisher = Publisher("test")
    book1.publisher = publisher
    book2.publisher = publisher
    repo.add_book(book1)
    repo.add_book(book2)

    books = repo.get_books_by_publisher(publisher.name)
    assert len(books) is 2
    assert books[0] is book1
    assert books[1] is book2


def test_repository_can_get_books_by_release(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book1 = Book(874658, "Harry Potter")
    book2 = Book(874659, "Harry Potter 1")

    book1.release_year = 2021
    book2.release_year = 2020
    repo.add_book(book1)
    repo.add_book(book2)

    books = repo.get_books_by_release_year(2021)

    assert len(books) is 1
    assert books[0] is book1


def test_repository_can_get_books_author_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book1 = Book(874658, "Harry Potter")
    author = Author(123, 'test author')
    book1.add_author(author)
    repo.add_book(book1)

    books = repo.get_books_by_author_id(123)

    assert len(books) is 1
    assert books[0] is book1


def test_repository_can_add_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    author = Author(123, 'test author')
    repo.add_author(author)

    result = repo.get_author(123)
    assert result.unique_id == author.unique_id
    assert result.full_name == author.full_name
    assert result.average_rating == author.average_rating
    assert result.text_reviews_count == author.text_reviews_count
    assert result.ratings_count == author.ratings_count


def test_repository_can_retrieve_an_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    author = Author(123, 'test author')
    repo.add_author(author)

    author1 = repo.get_author(123)
    assert author1.unique_id == author.unique_id
    assert author1.full_name == author.full_name
    assert author1.average_rating == author.average_rating
    assert author1.text_reviews_count == author.text_reviews_count
    assert author1.ratings_count == author.ratings_count


def test_repository_can_retrive_a_non_existent_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    author = repo.get_author(123)
    assert author is None


def test_repository_can_get_authors(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    author1 = Author(123, 'test author 1')
    repo.add_author(author1)
    author2 = Author(124, 'test author 2')
    repo.add_author(author2)

    authors = repo.get_authors(0, 2)
    assert len(authors) is 2


def test_repository_can_get_authors_number(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    authors_number = repo.get_number_of_authors()
    assert authors_number is 5


def test_repository_can_add_publisher(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    publisher = Publisher('test publisher')
    repo.add_publisher(publisher)
    assert repo.get_publisher(publisher.name) is publisher
