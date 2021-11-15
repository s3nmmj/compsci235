import json
from typing import List

from library.domain.model import Publisher, Author, Book


class BooksJSONReader:

    def __init__(self, books_file_name: str, authors_file_name: str):
        self.__books_file_name = books_file_name
        self.__authors_file_name = authors_file_name
        self.__dataset_of_books = []
        self.__dataset_of_authors = []

    @property
    def dataset_of_books(self) -> List[Book]:
        return self.__dataset_of_books

    @property
    def dataset_of_authors(self) -> List[Author]:
        return self.__dataset_of_authors

    def read_books_file(self) -> list:
        books_json = []
        with open(self.__books_file_name, encoding='UTF-8') as books_jsonfile:
            for line in books_jsonfile:
                book_entry = json.loads(line)
                books_json.append(book_entry)
        return books_json

    def read_authors_file(self) -> list:
        authors_json = []
        with open(self.__authors_file_name, encoding='UTF-8') as authors_jsonfile:
            for line in authors_jsonfile:
                author_entry = json.loads(line)
                authors_json.append(author_entry)
        return authors_json

    def read_json_files(self):
        authors_json = self.read_authors_file()
        for author_json in authors_json:
            author = Author(int(author_json['author_id']), author_json['name'])
            author.average_rating = float(author_json['average_rating'])
            author.text_reviews_count = int(author_json['text_reviews_count'])
            author.ratings_count = int(author_json['ratings_count'])
            self.__dataset_of_authors.append(author)

        books_json = self.read_books_file()

        for book_json in books_json:
            book_instance = Book(int(book_json['book_id']), book_json['title'])
            book_instance.publisher = Publisher(book_json['publisher'])
            if book_json['publication_year'] != '':
                book_instance.release_year = int(book_json['publication_year'])
            if book_json['is_ebook'].lower() == 'false':
                book_instance.ebook = False
            else:
                if book_json['is_ebook'].lower() == 'true':
                    book_instance.ebook = True
            book_instance.description = book_json['description']
            if book_json['num_pages'] != '':
                book_instance.num_pages = int(book_json['num_pages'])

            book_instance.image_url = None if book_json['image_url'] == '' else book_json['image_url']
            book_instance.isbn = None if book_json['isbn'] == '' else book_json['isbn']
            book_instance.link = None if book_json['link'] == '' else book_json['link']
            book_instance.ratings_count = None if book_json['ratings_count'] == '' else int(book_json['ratings_count'])
            book_instance.average_rating = None if book_json['average_rating'] == '' else float(
                book_json['average_rating'])
            book_instance.text_reviews_count = None if book_json['text_reviews_count'] == '' else int(
                book_json['text_reviews_count'])

            # extract the author ids:
            list_of_authors_ids = book_json['authors']
            for author_id in list_of_authors_ids:

                numerical_id = int(author_id['author_id'])
                # We assume book authors are available in the authors file,
                # otherwise more complex handling is required.
                author_name = None
                for author in self.dataset_of_authors:
                    if author.unique_id == numerical_id:
                        book_instance.add_author(author)
                        break

            self.__dataset_of_books.append(book_instance)
