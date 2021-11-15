from library.adapters.repository import AbstractRepository

default_page_size = 30


def get_authors(repo: AbstractRepository, offset: int = 0):
    return repo.get_authors(offset, default_page_size)


def get_number_of_authors(repo: AbstractRepository):
    return repo.get_number_of_authors()
