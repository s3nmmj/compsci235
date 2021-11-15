from pathlib import Path

from library.adapters.csv_data_importer import load_books_and_authors, load_users
from library.adapters.repository import AbstractRepository
from library.domain.model import Publisher


def populate(data_path: Path, repo: AbstractRepository):
    books, authors = load_books_and_authors(data_path)

    # add books
    for book in books:
        publisher = repo.add_publisher(Publisher(book.publisher.name))
        publisher.add_book(book)
        book.publisher = publisher
        repo.add_book(book)

    # Load users into the repository.
    users = load_users(data_path)
    for user in users:
        repo.add_user(user)

    # # add authors
    for author in authors:
        repo.add_author(author)
