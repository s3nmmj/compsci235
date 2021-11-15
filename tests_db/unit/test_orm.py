import pytest
from sqlalchemy.exc import IntegrityError

from library.domain.model import User, Author, Book, Publisher, Review, ReadingList


def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234567"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def make_user():
    user = User("Andrew", "1111111")
    return user


def test_loading_of_users(empty_session):
    users = list()
    users.append(("Andrew", "1234567"))
    users.append(("Cindy", "1111111"))
    insert_users(empty_session, users)

    expected = [
        User("Andrew", "1234567"),
        User("Cindy", "999")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session):
    user = User("Andrew", "1111111")
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [("Andrew", "1111111")]


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("Andrew", "1234567"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("Andrew", "1111111")
        empty_session.add(user)
        empty_session.commit()


def insert_authors(empty_session, values):
    for value in values:
        empty_session.execute(
            'INSERT INTO authors (unique_id, full_name, average_rating, text_reviews_count, ratings_count)'
            ' VALUES (:unique_id, :full_name, :average_rating, :text_reviews_count, :ratings_count)',
            {'unique_id': value[0],
             'full_name': value[1],
             'average_rating': value[2],
             'text_reviews_count': value[3],
             'ratings_count': value[4]})
    rows = list(empty_session.execute('SELECT unique_id from authors'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_author(empty_session, value):
    empty_session.execute(
        'INSERT INTO authors (unique_id, full_name, average_rating, text_reviews_count, ratings_count)'
        ' VALUES (:unique_id, :full_name, :average_rating, :text_reviews_count, :ratings_count)',
        {'unique_id': value[0],
         'full_name': value[1],
         'average_rating': value[2],
         'text_reviews_count': value[3],
         'ratings_count': value[4]})
    row = empty_session.execute('SELECT unique_id from authors where unique_id = :unique_id',
                                {'unique_id': value[0]}).fetchone()
    return row[0]


def make_author(unique_id, full_name, average_rating, text_reviews_count, ratings_count):
    author = Author(unique_id, full_name)
    author.average_rating = average_rating
    author.text_reviews_count = text_reviews_count
    author.ratings_count = ratings_count
    return author


def test_loading_of_authors(empty_session):
    authors = list()
    authors.append((163, 'Marguerite Duras', 3.74, 3509, 50771))
    authors.append((796, 'Sandra Lee', 3.46, 375, 2925))
    insert_authors(empty_session, authors)

    expected = [
        make_author(163, 'Marguerite Duras', 3.74, 3509, 50771),
        make_author(796, 'Sandra Lee', 3.46, 375, 2925)
    ]
    result = empty_session.query(Author).all()
    assert result == expected


def test_saving_of_authors(empty_session):
    author = make_author(163, 'Marguerite Duras', 3.74, 3509, 50771)
    empty_session.add(author)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT unique_id, full_name, average_rating, text_reviews_count, ratings_count'
                                      ' FROM authors'))
    assert rows == [(163, 'Marguerite Duras', 3.74, 3509, 50771)]


def test_saving_of_authors_with_common_author_id(empty_session):
    insert_author(empty_session, (163, 'Marguerite Duras', 3.74, 3509, 50771))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        author = make_author(163, 'Marguerite Duras', 3.74, 3509, 50771)
        empty_session.add(author)
        empty_session.commit()


def insert_books(empty_session, values):
    for value in values:
        empty_session.execute(
            'INSERT INTO books (book_id, title, release_year, description, ebook, num_pages, image_url, isbn, link, '
            'ratings_count, average_rating, text_reviews_count, publisher_name)'
            ' VALUES (:book_id, :title, :release_year, :description, :ebook, :num_pages, :image_url, :isbn, :link, '
            ':ratings_count, :average_rating, :text_reviews_count, :publisher_name)',
            {'book_id': value[0],
             'title': value[1],
             'release_year': value[2],
             'description': value[3],
             'ebook': value[4],
             'num_pages': value[5],
             'image_url': value[6],
             'isbn': value[7],
             'link': value[8],
             'ratings_count': value[9],
             'average_rating': value[10],
             'text_reviews_count': value[11],
             'publisher_name': value[12]})
    rows = list(empty_session.execute('SELECT book_id from books'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_book(empty_session, value):
    empty_session.execute(
        'INSERT INTO books (book_id, title, release_year, description, ebook, num_pages, image_url, isbn, link, '
        'ratings_count, average_rating, text_reviews_count, publisher_name)'
        ' VALUES (:book_id, :title, :release_year, :description, :ebook, :num_pages, :image_url, :isbn, :link, '
        ':ratings_count, :average_rating, :text_reviews_count, :publisher_name)',
        {'book_id': value[0],
         'title': value[1],
         'release_year': value[2],
         'description': value[3],
         'ebook': value[4],
         'num_pages': value[5],
         'image_url': value[6],
         'isbn': value[7],
         'link': value[8],
         'ratings_count': value[9],
         'average_rating': value[10],
         'text_reviews_count': value[11],
         'publisher_name': value[12]})
    row = empty_session.execute('SELECT book_id from books where book_id = :book_id',
                                {'book_id': value[0]}).fetchone()
    return row[0]


def make_book(book_id, title, release_year, description, ebook, num_pages, image_url, isbn, link, ratings_count,
              average_rating, text_reviews_count, publisher_name):
    book = Book(book_id, title)
    book.description = description
    book.publisher = Publisher(publisher_name)
    book.release_year = release_year
    book.ebook = ebook
    book.num_pages = num_pages

    book.image_url = image_url
    book.isbn = isbn
    book.link = link
    book.ratings_count = ratings_count
    book.average_rating = average_rating
    book.text_reviews_count = text_reviews_count
    return book


def test_loading_of_books(empty_session):
    books = list()
    books.append((707611, "Superman Archives, Vol. 2", 1997,
                  "These are the stories that catapulted Superman into the spotlight as one of the world's premier heroes of fiction. These volumes feature his earliest adventures, when the full extent of his powers was still developing and his foes were often bank robbers and crooked politicians.",
                  0, 272, "https://images.gr-assets.com/books/1307838888m/707611.jpg", "0930289765",
                  "https://www.goodreads.com/book/show/707611.Superman_Archives_Vol_2", 51, 4.06, 6, "DC Comics"
                  ))
    books.append((2168737, "The Thing: Idol of Millions", 2006,
                  "Join Ben Grimm and his pals as they clobber their way through the Marvel Universe! Spinning out of events from 'Fantastic Four', the idol of millions is now worth billions - but will big bucks make a Rockefeller out of this rocky fella?",
                  0, 192, "https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png",
                  "0785118136", "https://www.goodreads.com/book/show/2168737.The_Thing", 86, 3.8, 13, "Marvel"))
    insert_books(empty_session, books)

    expected = [
        make_book(707611, "Superman Archives, Vol. 2", 1997,
                  "These are the stories that catapulted Superman into the spotlight as one of the world's premier heroes of fiction. These volumes feature his earliest adventures, when the full extent of his powers was still developing and his foes were often bank robbers and crooked politicians.",
                  0, 272, "https://images.gr-assets.com/books/1307838888m/707611.jpg", "0930289765",
                  "https://www.goodreads.com/book/show/707611.Superman_Archives_Vol_2", 51, 4.06, 6, "DC Comics"
                  ),
        make_book(2168737, "The Thing: Idol of Millions", 2006,
                  "Join Ben Grimm and his pals as they clobber their way through the Marvel Universe! Spinning out of events from 'Fantastic Four', the idol of millions is now worth billions - but will big bucks make a Rockefeller out of this rocky fella?",
                  0, 192, "https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png",
                  "0785118136", "https://www.goodreads.com/book/show/2168737.The_Thing", 86, 3.8, 13, "Marvel")
    ]
    result = empty_session.query(Book).all()
    assert result == expected


def test_saving_of_books(empty_session):
    book = make_book(2168737, "The Thing: Idol of Millions", 2006,
                     "Join Ben Grimm and his pals as they clobber their way through the Marvel Universe! Spinning out of events from 'Fantastic Four', the idol of millions is now worth billions - but will big bucks make a Rockefeller out of this rocky fella?",
                     0, 192, "https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png",
                     "0785118136", "https://www.goodreads.com/book/show/2168737.The_Thing", 86, 3.8, 13, "Marvel")
    empty_session.add(book)
    empty_session.commit()

    rows = list(empty_session.execute(
        'SELECT book_id, title, release_year, description, ebook, num_pages, image_url, isbn, link, '
        'ratings_count, average_rating, text_reviews_count, publisher_name'
        ' FROM books'))
    assert rows == [(2168737, "The Thing: Idol of Millions", 2006,
                     "Join Ben Grimm and his pals as they clobber their way through the Marvel Universe! Spinning out of events from 'Fantastic Four', the idol of millions is now worth billions - but will big bucks make a Rockefeller out of this rocky fella?",
                     0, 192, "https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png",
                     "0785118136", "https://www.goodreads.com/book/show/2168737.The_Thing", 86, 3.8, 13, "Marvel")]


def test_saving_of_books_with_common_book_id(empty_session):
    insert_book(empty_session, (2168737, "The Thing: Idol of Millions", 2006,
                                "Join Ben Grimm and his pals as they clobber their way through the Marvel Universe! Spinning out of events from 'Fantastic Four', the idol of millions is now worth billions - but will big bucks make a Rockefeller out of this rocky fella?",
                                0, 192,
                                "https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png",
                                "0785118136", "https://www.goodreads.com/book/show/2168737.The_Thing", 86, 3.8, 13,
                                "Marvel"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        book = make_book(2168737, "The Thing: Idol of Millions", 2006,
                         "Join Ben Grimm and his pals as they clobber their way through the Marvel Universe! Spinning out of events from 'Fantastic Four', the idol of millions is now worth billions - but will big bucks make a Rockefeller out of this rocky fella?",
                         0, 192,
                         "https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png",
                         "0785118136", "https://www.goodreads.com/book/show/2168737.The_Thing", 86, 3.8, 13, "Marvel")
        empty_session.add(book)
        empty_session.commit()


def insert_reviews(empty_session, values):
    for value in values:
        empty_session.execute(
            'INSERT INTO reviews (id, review, "timestamp", user_id, book_id)'
            ' VALUES (:id, :review, :timestamp, :user_id, :book_id)',
            {'id': value[0],
             'review': value[1],
             'timestamp': value[2],
             'user_id': value[3],
             'book_id': value[4]})
    rows = list(empty_session.execute('SELECT id from reviews'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_review(empty_session, value):
    empty_session.execute(
        'INSERT INTO reviews (id, review, "timestamp", user_id, book_id)'
        ' VALUES (:id, :review, :timestamp, :user_id, :book_id)',
        {'id': value[0],
         'review': value[1],
         'timestamp': value[2],
         'user_id': value[3],
         'book_id': value[4]})

    row = empty_session.execute('SELECT id from reviews where id = :id',
                                {'id': value[0]}).fetchone()
    return row[0]


def make_review(user, book, review):
    review = Review(user, book, review)
    return review


def test_loading_of_reviews(empty_session):
    book = make_book(2168737, "The Thing: Idol of Millions", 2006,
                     "Join Ben Grimm and his pals as they clobber their way through the Marvel Universe! Spinning out of events from 'Fantastic Four', the idol of millions is now worth billions - but will big bucks make a Rockefeller out of this rocky fella?",
                     0, 192,
                     "https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png",
                     "0785118136", "https://www.goodreads.com/book/show/2168737.The_Thing", 86, 3.8, 13, "Marvel")

    user = User("Andrew", "1111111")

    reviews = list()
    reviews.append((1, "test123", "2021-10-18 15:22:38.202558", 1, 2168737))
    reviews.append((2, "test456", "2021-10-18 15:22:44.430866", 1, 2168737))
    insert_reviews(empty_session, reviews)

    expected = [
        make_review(user, book, "test123"),
        make_review(user, book, "test456")
    ]
    result = empty_session.query(Review).all()
    assert len(result) == len(expected)
    for i in range(len(result)):
        result[i].review == expected[i].review


def test_saving_of_reviews(empty_session):
    insert_book(empty_session, (2168737, "The Thing: Idol of Millions", 2006,
                                "Join Ben Grimm and his pals as they clobber their way through the Marvel Universe! Spinning out of events from 'Fantastic Four', the idol of millions is now worth billions - but will big bucks make a Rockefeller out of this rocky fella?",
                                0, 192,
                                "https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png",
                                "0785118136", "https://www.goodreads.com/book/show/2168737.The_Thing", 86, 3.8,
                                13, "Marvel"))
    book = empty_session.query(Book).one()

    insert_user(empty_session, ("Andrew", "1111111"))
    user = empty_session.query(User).one()

    review = make_review(user, book, "test")
    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT id, review, "timestamp", user_id, book_id'
                                      ' FROM reviews'))
    assert len(rows) == 1
    assert rows[0].id == 1
    assert rows[0].user_id == 1
    assert rows[0].book_id == 2168737


def insert_reading_lists(empty_session, values):
    for value in values:
        empty_session.execute(
            'INSERT INTO user_reading_lists (id, shelf, user_id, book_id)'
            ' VALUES (:id, :shelf, :user_id, :book_id)',
            {'id': value[0],
             'shelf': value[1],
             'user_id': value[2],
             'book_id': value[3]})
    rows = list(empty_session.execute('SELECT id from user_reading_lists'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_reading_list(empty_session, value):
    empty_session.execute(
        'INSERT INTO user_reading_lists (id, shelf, user_id, book_id)'
        ' VALUES (:id, :shelf, :user_id, :book_id)',
        {'id': value[0],
         'shelf': value[1],
         'user_id': value[2],
         'book_id': value[3]})

    row = empty_session.execute('SELECT id from user_reading_lists where id = :id',
                                {'id': value[0]}).fetchone()
    return row[0]


def make_reading_list(user, book, shelf):
    reading_list = ReadingList(user, book, shelf)
    return reading_list


def test_saving_of_reading_list(empty_session):
    insert_book(empty_session, (2168737, "The Thing: Idol of Millions", 2006,
                                "Join Ben Grimm and his pals as they clobber their way through the Marvel Universe! Spinning out of events from 'Fantastic Four', the idol of millions is now worth billions - but will big bucks make a Rockefeller out of this rocky fella?",
                                0, 192,
                                "https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png",
                                "0785118136", "https://www.goodreads.com/book/show/2168737.The_Thing", 86, 3.8,
                                13, "Marvel"))
    book = empty_session.query(Book).one()

    insert_user(empty_session, ("Andrew", "1111111"))
    user = empty_session.query(User).one()

    expected = [
        make_reading_list(user, book, "Currently Reading"),
    ]
    result = empty_session.query(ReadingList).all()
    assert result == expected
