from datetime import date

import pytest

from library.authentication.services import AuthenticationException
from library.authentication import services as auth_services
from library.book import services as book_service
from library.book.services import NonExistentBookException
from library.book.services import UnknownUserException
from library.author import services as author_service
from library.domain.model import ShelfName


def test_can_add_user(in_memory_repo):
    new_user_name = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_user_name, in_memory_repo)
    assert user_as_dict['user_name'] == new_user_name

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    user_name = 'thorke'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(user_name, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_user_name, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, '0987654321', in_memory_repo)


def test_can_get_book(in_memory_repo):
    book_id = 25742454
    book = book_service.get_book_by_id(in_memory_repo, book_id)

    assert book.book_id == book_id
    assert len(book.authors) == 1
    assert book.authors[0].full_name == 'Lindsey Schussman'
    assert book.average_rating == 4.12
    assert book.description == '''Lillian Ann Cross is forced to live the worst nightmare of her life. She is an everyday middle class American, striving to survive in an everyday changing world. Her life was abruptly
turned upsidedown forever as she was kidnapped and forced into a world called "Hen Fighting."
A world in which women fight and bets are made upon their bloodshed.Lillian is forced to comply due to the threats made upon her mother's life. Being a loving person her whole life, Lillian finds difficulty grasping her new functions. As she is conditioned to live in her new world, she is subjected to an experimental procedure. A procedure which has taken the lives of a few before her. As she survives, she now has to learn how to live with her new "implants." Implants which strengthen her bones, giving her strength and an upper ability amongst others. Implants which require weekly sustenance, or she will die.'''
    assert book.image_url == 'https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png'
    assert book.link == 'https://www.goodreads.com/book/show/25742454-the-switchblade-mamma'
    assert book.ratings_count == 1
    assert book.release_year is None
    assert book.text_reviews_count == 1
    assert book.title == 'The Switchblade Mamma'
    assert book.publisher.name == 'N/A'


def test_can_get_books(in_memory_repo):
    books = book_service.get_books(in_memory_repo)
    assert len(books) == 3


def test_can_get_books_by_publisher(in_memory_repo):
    books = book_service.get_books_by_publisher(in_memory_repo, 'N/A')
    assert len(books) == 2
    books = book_service.get_books_by_publisher(in_memory_repo, 'Dargaud')
    assert len(books) == 1


def test_can_get_books_by_release_year(in_memory_repo):
    books = book_service.get_books_by_release_year(in_memory_repo, 2014)
    assert len(books) == 1
    books = book_service.get_books_by_release_year(in_memory_repo, 2016)
    assert len(books) == 1


def test_can_get_books_by_author_id(in_memory_repo):
    books = book_service.get_books_by_author_id(in_memory_repo, 8551671)
    assert len(books) == 1
    book = books[0]
    assert book.authors[0].full_name == 'Lindsey Schussman'
    assert book.average_rating == 4.12
    assert book.description == '''Lillian Ann Cross is forced to live the worst nightmare of her life. She is an everyday middle class American, striving to survive in an everyday changing world. Her life was abruptly
turned upsidedown forever as she was kidnapped and forced into a world called "Hen Fighting."
A world in which women fight and bets are made upon their bloodshed.Lillian is forced to comply due to the threats made upon her mother's life. Being a loving person her whole life, Lillian finds difficulty grasping her new functions. As she is conditioned to live in her new world, she is subjected to an experimental procedure. A procedure which has taken the lives of a few before her. As she survives, she now has to learn how to live with her new "implants." Implants which strengthen her bones, giving her strength and an upper ability amongst others. Implants which require weekly sustenance, or she will die.'''
    assert book.image_url == 'https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png'
    assert book.link == 'https://www.goodreads.com/book/show/25742454-the-switchblade-mamma'
    assert book.ratings_count == 1
    assert book.release_year is None
    assert book.text_reviews_count == 1
    assert book.title == 'The Switchblade Mamma'
    assert book.publisher.name == 'N/A'


def test_can_get_number_of_books(in_memory_repo):
    books = book_service.get_number_of_books(in_memory_repo)
    assert books == 3


def test_can_add_review_raise_exception(in_memory_repo):
    book_id = 8551671
    with pytest.raises(book_service.NonExistentBookException):
        book_service.add_review(book_id, 'test review', 'thorke', in_memory_repo)


def test_can_add_and_get_review(in_memory_repo):
    book_id = 25742454
    book_service.add_review(book_id, 'test review', 'thorke', in_memory_repo)
    reviews = book_service.get_reviews_by_book_id(in_memory_repo, book_id)

    assert len(reviews) == 1
    assert reviews[0].review == 'test review'
    assert reviews[0].user == in_memory_repo.get_user('thorke')


def test_can_add_book_to_user_raise_exception(in_memory_repo):
    with pytest.raises(book_service.NonExistentBookException):
        book_service.add_book_to_user('test', 123, ShelfName.READ.value, in_memory_repo)

    with pytest.raises(book_service.UnknownUserException):
        book_service.add_book_to_user('test', 25742454, ShelfName.READ.value, in_memory_repo)


def test_can_add_book_to_and_get_from_user(in_memory_repo):
    book_service.add_book_to_user('thorke', 25742454, ShelfName.READ.value, in_memory_repo)
    books = book_service.get_books_by_user_and_shelf(in_memory_repo, 'thorke', ShelfName.READ)
    assert len(books) == 1
    assert books[0].book_id == 25742454


def test_can_get_books_by_user_and_shelf_raise_exception(in_memory_repo):
    with pytest.raises(book_service.UnknownUserException):
        book_service.get_books_by_user_and_shelf(in_memory_repo, 'thorke1', ShelfName.READ)


def test_can_get_authors(in_memory_repo):
    authors = author_service.get_authors(in_memory_repo)
    assert len(authors) == 5


def test_can_get_number_of_authors(in_memory_repo):
    authors = author_service.get_number_of_authors(in_memory_repo)
    assert authors == 5
