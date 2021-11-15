import random

from library.adapters.repository import AbstractRepository


def get_random_books(quantity, repo: AbstractRepository):
    book_count = repo.get_number_of_books()

    if quantity >= book_count:
        # Reduce the quantity of ids to generate if the repository has an insufficient number of books.
        quantity = book_count - 1

    # Pick distinct and random articles.
    random_indices = random.sample(range(0, book_count), quantity)
    books = repo.get_books_by_indices(random_indices)

    return books

