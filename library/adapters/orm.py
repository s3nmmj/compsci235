# global variable giving access to the MetaData (schema) information of the database
from sqlalchemy import MetaData, Table, Column, Integer, String, Float, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import mapper, relationship, backref

from library.domain import model

metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reading_lists_table = Table(
    'user_reading_lists', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('shelf', String(255), nullable=False),
    Column('book_id', ForeignKey('books.book_id')),
    Column('user_id', ForeignKey('users.id'))
)

publishers_table = Table(
    'publishers', metadata,
    Column('name', String(255), primary_key=True, nullable=False),
)

authors_table = Table(
    'authors', metadata,
    Column('unique_id', Integer, primary_key=True, nullable=False),
    Column('full_name', String(255), nullable=False),
    Column('average_rating', Float, nullable=False, default=0.0),
    Column('text_reviews_count', Integer, nullable=False, default=0),
    Column('ratings_count', Integer, nullable=False, default=0),
)

books_table = Table(
    'books', metadata,
    Column('book_id', Integer, primary_key=True, nullable=False),
    Column('title', String(1024), nullable=False),
    Column('release_year', Integer, nullable=True),
    Column('description', String(1024), nullable=True),
    Column('ebook', Boolean, nullable=False, default=False),
    Column('num_pages', Integer, nullable=True),
    Column('image_url', String(1024), nullable=True),
    Column('isbn', String(1024), nullable=True),
    Column('link', String(1024), nullable=True),
    Column('ratings_count', Integer, nullable=True),
    Column('average_rating', Float, nullable=True),
    Column('text_reviews_count', Integer, nullable=True),
    Column('publisher_name', ForeignKey('publishers.name')),
)

book_authors_table = Table(
    'book_authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_id', ForeignKey('books.book_id')),
    Column('author_id', ForeignKey('authors.unique_id'))
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('review', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=False),
    Column('user_id', ForeignKey('users.id')),
    Column('book_id', ForeignKey('books.book_id')),
)


def map_model_to_tables():
    mapper(model.User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(model.Review, backref='_Review__user'),
        '_User__reading_lists': relationship(model.ReadingList, backref='_ReadingList__user'),
    })

    mapper(model.ReadingList, reading_lists_table, properties={
        '_ReadingList__shelf': reading_lists_table.c.shelf,
    })

    mapper(model.Review, reviews_table, properties={
        '_Review__review': reviews_table.c.review,
        '_Review__timestamp': reviews_table.c.timestamp,
    })

    mapper(model.Publisher, publishers_table, properties={
        '_Publisher__name': publishers_table.c.name,
        '_Publisher__books': relationship(model.Book, backref='_Book__publisher', cascade="merge")
    })

    mapper(model.Book, books_table, properties={
        '_Book__book_id': books_table.c.book_id,
        '_Book__title': books_table.c.title,
        '_Book__release_year': books_table.c.release_year,
        '_Book__description': books_table.c.description,
        '_Book__ebook': books_table.c.ebook,
        '_Book__num_pages': books_table.c.num_pages,
        '_Book__image_url': books_table.c.image_url,
        '_Book__isbn': books_table.c.isbn,
        '_Book__link': books_table.c.link,
        '_Book__ratings_count': books_table.c.ratings_count,
        '_Book__average_rating': books_table.c.average_rating,
        '_Book__text_reviews_count': books_table.c.text_reviews_count,
        '_Book__authors': relationship(model.Author, secondary=book_authors_table),
        '_Book__reviews': relationship(model.Review, backref='_Review__book'),
        '_Book__reading_lists': relationship(model.ReadingList, backref='_ReadingList__book'),
    })

    mapper(model.Author, authors_table, properties={
        '_Author__unique_id': authors_table.c.unique_id,
        '_Author__full_name': authors_table.c.full_name,
        '_Author__average_rating': authors_table.c.average_rating,
        '_Author__text_reviews_count': authors_table.c.text_reviews_count,
        '_Author__ratings_count': authors_table.c.ratings_count,
        '_Author__books': relationship(
            model.Book,
            secondary=book_authors_table
        )
    })
