import pytest

from flask import session


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid user name and password.
    response = client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
        ('fmercury', 'Test#6^0', b'Your user name is already taken - please supply another'),
))
def test_register_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['user_name'] == 'thorke'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200


def test_login_required_to_review(client):
    response = client.post('/review')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_login_required_to_my_books(client):
    response = client.post('/my_books')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_review(client, auth):
    # Login a user.
    auth.login()

    response = client.post(
        '/review',
        data={'review': 'this is a test review', 'book_id': 25742454}
    )
    assert response.headers['Location'] == 'http://localhost/books?book_id=25742454&search_type=book'


def test_get_book_by_id(client):
    # Check that we can retrieve the articles page.
    response = client.get('/books?book_id=25742454&search_type=book')
    assert response.status_code == 200

    assert b'The Switchblade Mamma' in response.data


def test_get_book_by_publisher(client):
    # Check that we can retrieve the articles page.
    response = client.get('/books?publisher_name=Dargaud&search_type=publisher')
    assert response.status_code == 200

    assert b'Cruelle' in response.data
    assert b'Dargaud' in response.data


def test_get_book_by_release_year(client):
    # Check that we can retrieve the articles page.
    response = client.get('/books?release_year=2016&search_type=release_year')
    assert response.status_code == 200

    assert b'Cruelle' in response.data
    assert b'Dargaud' in response.data


def test_get_book_by_author_id(client):
    # Check that we can retrieve the articles page.
    response = client.get('/books?author_id=8551671&search_type=author')
    assert response.status_code == 200

    assert b'The Switchblade Mamma' in response.data


def test_my_books(client, auth):
    # Login a user.
    auth.login()

    response = client.get('/my_books')
    assert response.status_code == 200

    assert b'Empty!' in response.data
    assert b'Currently Reading' in response.data
    assert b'Want to Read' in response.data
    assert b'Read' in response.data


def test_add_to_booking_list(client, auth):
    # Login a user.
    auth.login()

    response = client.post(
        '/my_books',
        data={'reading_list': 'Read', 'book_id': 25742454}
    )
    assert response.headers['Location'] == 'http://localhost/books?book_id=25742454&search_type=book'

    response = client.get('/my_books?shelf=read')
    assert response.status_code == 200

    assert b'Currently Reading' in response.data
    assert b'Want to Read' in response.data
    assert b'Read' in response.data
    assert b'The Switchblade Mamma' in response.data


def test_get_books(client, auth):
    # Check that we can retrieve the articles page.
    response = client.get('/books')
    assert response.status_code == 200

    assert b'The Switchblade Mamma' in response.data
    assert b'Cruelle' in response.data
    assert b'The Breaker New Waves, Vol 11' in response.data


def test_get_authors(client, auth):
    # Check that we can retrieve the articles page.
    response = client.get('/authors')
    assert response.status_code == 200

    assert b'Ronald J. Fields' in response.data
    assert b'Anita Diamant' in response.data
    assert b'Gerard Lelarge' in response.data
    assert b'Jean-Claude Biver' in response.data
    assert b'Lindsey Schussman' in response.data
