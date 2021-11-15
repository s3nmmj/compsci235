import csv
from pathlib import Path

from werkzeug.security import generate_password_hash

from library.adapters.jsondatareader import BooksJSONReader
from library.domain.model import User


def load_books_and_authors(data_path: Path):
    books_file_name = 'comic_books_excerpt.json'
    authors_file_name = 'book_authors_excerpt.json'

    path_to_books_file = str(data_path / books_file_name)
    path_to_authors_file = str(data_path / authors_file_name)
    reader = BooksJSONReader(path_to_books_file, path_to_authors_file)
    reader.read_json_files()
    return reader.dataset_of_books, reader.dataset_of_authors


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_users(data_path: Path):
    users = list()

    users_filename = str(Path(data_path) / "users.csv")
    for data_row in read_csv_file(users_filename):
        user = User(
            user_name=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        users.append(user)
    return users

