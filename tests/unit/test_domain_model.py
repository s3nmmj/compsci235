import datetime
from pathlib import Path
import pytest

from utils import get_project_root

from library.domain.model import Publisher, Author, Book, User, Review, ShelfName
from library.adapters.jsondatareader import BooksJSONReader


class TestPublisher:

    def test_construction(self):
        publisher1 = Publisher("Avatar Press")
        assert str(publisher1) == "<Publisher Avatar Press>"

        publisher2 = Publisher("  ")
        assert str(publisher2) == "<Publisher N/A>"

        publisher3 = Publisher("  DC Comics ")
        assert str(publisher3) == "<Publisher DC Comics>"

        publisher4 = Publisher(42)
        assert str(publisher4) == "<Publisher N/A>"

    def test_comparison(self):
        publisher1 = Publisher("Avatar Press")
        publisher2 = Publisher("DC Comics")
        publisher3 = Publisher("Avatar Press")
        publisher4 = Publisher("")
        assert str(publisher4) == "<Publisher N/A>"
        assert publisher1 == publisher3
        assert publisher1 != publisher2
        assert publisher3 != publisher2
        assert publisher2 != publisher3

    def test_sorting(self):
        publisher1 = Publisher("Avatar Press")
        publisher2 = Publisher("Penguin Books")
        publisher3 = Publisher("DC Comics")
        assert publisher1 < publisher2
        assert publisher1 < publisher3
        assert publisher2 > publisher3

    def test_set_operations(self):
        publisher1 = Publisher("Avatar Press")
        publisher2 = Publisher("DC Comics")
        publisher3 = Publisher("Avatar Press")
        set_of_publisher = set()
        set_of_publisher.add(publisher1)
        set_of_publisher.add(publisher2)
        set_of_publisher.add(publisher3)
        assert str(sorted(set_of_publisher)) == "[<Publisher Avatar Press>, <Publisher DC Comics>]"

    def test_attribute_setters(self):
        publisher1 = Publisher("Avatar Press")
        assert str(publisher1) == "<Publisher Avatar Press>"
        assert publisher1.name == "Avatar Press"
        publisher1.name = "DC Comics"
        assert str(publisher1) == "<Publisher DC Comics>"


class TestAuthor:

    def test_construction(self):
        author = Author(3675, "J.R.R. Tolkien")
        assert str(author) == "<Author J.R.R. Tolkien, author id = 3675>"

        with pytest.raises(ValueError):
            author = Author(123, "  ")

        with pytest.raises(ValueError):
            author = Author(42, 42)

    def test_comparison(self):
        author1 = Author(1, "J.R.R. Tolkien")
        author2 = Author(2, "Neil Gaiman")
        author3 = Author(3, "J.K. Rowling")
        assert author1 != author3
        assert author1 != author2
        assert author3 != author2

    def test_comparison_with_identical_author_ids(self):
        # for two authors to be the same, our specification just asks for the unique id to match!
        author1 = Author(1, "Angelina Jolie")
        author2 = Author(2, "Angelina Jolie")
        author3 = Author(1, "J.K. Rowling")
        assert author1 == author3
        assert author1 != author2
        assert author3 != author2

    def test_sorting_names_and_ids_same_sort_order(self):
        author1 = Author(1, "J.K. Rowling")
        author2 = Author(2, "J.R.R. Tolkien")
        author3 = Author(3, "Neil Gaiman")
        assert author1 < author2
        assert author1 < author3
        assert author3 > author2

    def test_sorting_names_and_ids_differ_in_sort_order(self):
        author1 = Author(1, "Neil Gaiman")
        author2 = Author(2, "J.K. Rowling")
        author3 = Author(3, "J.R.R. Tolkien")
        assert author1 < author2
        assert author1 < author3
        assert author3 > author2

    def test_sorting_names_are_alphabetical(self):
        author1 = Author(13, "J.R.R. Tolkien")
        author2 = Author(2, "Neil Gaiman")
        author3 = Author(98, "J.K. Rowling")
        assert author1 > author2
        assert author1 < author3
        assert author3 > author2

    def test_set_operations(self):
        author1 = Author(13, "J.R.R. Tolkien")
        author2 = Author(2, "Neil Gaiman")
        author3 = Author(98, "J.K. Rowling")
        set_of_authors = set()
        set_of_authors.add(author1)
        set_of_authors.add(author2)
        set_of_authors.add(author3)
        assert str(sorted(
            set_of_authors)) == "[<Author Neil Gaiman, author id = 2>, <Author J.R.R. Tolkien, author id = 13>, <Author J.K. Rowling, author id = 98>]"

    def test_invalid_author_ids(self):
        author = Author(0, "J.R.R. Tolkien")
        assert str(author) == "<Author J.R.R. Tolkien, author id = 0>"

        with pytest.raises(ValueError):
            author = Author(-1, "J.R.R. Tolkien")

        with pytest.raises(ValueError):
            author = Author(13.786, "J.R.R. Tolkien")

        with pytest.raises(ValueError):
            author = Author(Publisher("DC Comics"), "J.R.R. Tolkien")

    def test_attribute_setters(self):
        author1 = Author(3675, "Barack Obama")
        assert str(author1) == "<Author Barack Obama, author id = 3675>"
        author1.full_name = "J.R.R. Tolkien"
        assert str(author1) == "<Author J.R.R. Tolkien, author id = 3675>"
        with pytest.raises(AttributeError):
            author1.unique_id = 12


class TestBook:

    def test_construction_modification(self):
        book = Book(84765876, "Harry Potter")
        assert str(book) == "<Book Harry Potter, book id = 84765876>"

        publisher = Publisher("Bloomsbury")
        book.publisher = publisher
        assert str(book.publisher) == "<Publisher Bloomsbury>"
        assert isinstance(book.publisher, Publisher)

        book = Book(1, "    Harry Potter    ")
        assert str(book) == "<Book Harry Potter, book id = 1>"

    def test_adding_author(self):
        book = Book(84765876, "Harry Potter")
        author = Author(635, "J.K. Rowling")
        book.add_author(author)
        assert isinstance(book.authors, list)
        assert isinstance(book.authors[0], Author)
        assert str(book.authors) == "[<Author J.K. Rowling, author id = 635>]"

    def test_attribute_setters(self):
        book = Book(84765876, "Harry Potter")
        book.description = "    Harry Potter was a highly unusual boy in many ways. For one thing, he hated the summer holidays more than any other time of year. For another, he really wanted to do his homework but was forced to do it in secret, in the dead of night. And he also happened to be a wizard.     "
        assert book.description == "Harry Potter was a highly unusual boy in many ways. For one thing, he hated the summer holidays more than any other time of year. For another, he really wanted to do his homework but was forced to do it in secret, in the dead of night. And he also happened to be a wizard."
        book.release_year = 1930
        assert book.release_year == 1930
        book.ebook = True
        assert book.ebook is True
        book.num_pages = 130
        assert book.num_pages == 130

    def test_attributes_fail(self):
        book = Book(84765876, "Harry Potter")

        book.num_pages = -1
        assert book.num_pages is None

        with pytest.raises(ValueError):
            book.release_year = -12

        with pytest.raises(ValueError):
            book.release_year = 3.5

        with pytest.raises(ValueError):
            book.title = 42

        with pytest.raises(AttributeError):
            book.book_id = 12

    def test_invalid_title(self):
        with pytest.raises(ValueError):
            book = Book(84765876, "")
        with pytest.raises(ValueError):
            book = Book(84765876, Publisher("DC Comics"))

    def test_invalid_book_ids(self):
        book = Book(0, "Harry Potter")
        assert str(book) == "<Book Harry Potter, book id = 0>"

        with pytest.raises(ValueError):
            book = Book(-1, "Harry Potter")

        with pytest.raises(ValueError):
            book = Book(13.786, "Harry Potter")

        with pytest.raises(ValueError):
            book = Book(Publisher("DC Comics"), "Harry Potter")

    def test_sorting(self):
        book1 = Book(874658, "Harry Potter")
        book2 = Book(2675376, "Hitchhiker's Guide to the Galaxy")
        book3 = Book(89576, "West Side Story")
        assert book1 < book2
        assert book1 > book3
        assert book2 > book3

    def test_set(self):
        book1 = Book(874658, "Harry Potter")
        book2 = Book(2675376, "Hitchhiker's Guide to the Galaxy")
        book3 = Book(89576, "West Side Story")
        set_of_books = set()
        set_of_books.add(book1)
        set_of_books.add(book2)
        set_of_books.add(book3)
        assert str(sorted(
            set_of_books)) == "[<Book West Side Story, book id = 89576>, <Book Harry Potter, book id = 874658>, <Book Hitchhiker's Guide to the Galaxy, book id = 2675376>]"

    def test_comparison(self):
        book1 = Book(874658, "Harry Potter")
        book2 = Book(2675376, "Hitchhiker's Guide to the Galaxy")
        book3 = Book(89576, "Harry Potter")
        book4 = Book(89576, "West Side Story")
        assert book1 != book2
        assert book1 != book3
        assert book3 == book4

    def test_remove_author(self):
        book = Book(89576, "Harry Potter")

        author1 = Author(1, "J.R.R. Tolkien")
        author2 = Author(2, "Neil Gaiman")
        author3 = Author(3, "Ernest Hemingway")
        author4 = Author(4, "J.K. Rowling")

        authors = [author1, author2, author3, author4]
        for author in authors:
            book.add_author(author)

        assert str(
            book.authors) == "[<Author J.R.R. Tolkien, author id = 1>, <Author Neil Gaiman, author id = 2>, <Author Ernest Hemingway, author id = 3>, <Author J.K. Rowling, author id = 4>]"

        # remove an Author who is not in the list
        book.remove_author(Author(5, "George Orwell"))
        assert str(
            book.authors) == "[<Author J.R.R. Tolkien, author id = 1>, <Author Neil Gaiman, author id = 2>, <Author Ernest Hemingway, author id = 3>, <Author J.K. Rowling, author id = 4>]"

        # remove an Author who is in the list
        book.remove_author(author2)
        assert str(
            book.authors) == "[<Author J.R.R. Tolkien, author id = 1>, <Author Ernest Hemingway, author id = 3>, <Author J.K. Rowling, author id = 4>]"


class TestReview:

    def test_construction(self):
        book = Book(2675376, "Harry Potter")
        review = "  This book was very enjoyable.   "
        user = User('username', 'password')
        review = Review(user, book, review)

        assert str(review.book) == "<Book Harry Potter, book id = 2675376>"
        assert str(review.review) == "This book was very enjoyable."
        assert str(review.user.user_name) == 'username'

    def test_set_of_reviews(self):
        book1 = Book(2675376, "Harry Potter")
        book2 = Book(874658, "Lord of the Rings")
        user = User('username', 'password')
        review1 = Review(user, book1, "I liked this book")
        review2 = Review(user, book2, "This book was ok")
        review3 = Review(user, book1, "This book was exceptional")
        assert review1 != review2
        assert review1 != review3
        assert review3 != review2

    def test_wrong_book_object(self):
        publisher = Publisher("DC Comics")
        user = User('username', 'password')
        review = Review(user, publisher, "I liked this book")
        assert review.book is None


class TestUser:

    def test_construction(self):
        user1 = User('Shyamli', 'pw12345')
        user2 = User('Martin', 'pw67890')
        user3 = User('Daniel', 'pw87465')
        assert str(user1) == "<User Shyamli>"
        assert str(user2) == "<User Martin>"
        assert str(user3) == "<User Daniel>"

    def test_sort_ordering(self):
        user1 = User("Shyamli", "pw12345")
        user2 = User("Martin", "pw67890")
        user3 = User("daniel", "pw12345")
        assert user1 > user2
        assert user3 > user1
        assert user3 > user2

    def test_comparison(self):
        user1 = User("Martin", "pw12345")
        user2 = User("Shyamli", "pw67890")
        user3 = User("martin", "pw45673")
        assert user1 != user3
        assert user1 != user2
        assert user3 != user2

    def test_set_operations(self):
        user1 = User('Shyamli', 'pw12345')
        user2 = User('Martin', 'pw67890')
        user3 = User('Daniel', 'pw87465')
        set_of_users = set()
        set_of_users.add(user1)
        set_of_users.add(user2)
        set_of_users.add(user3)
        assert str(sorted(set_of_users)) == "[<User Daniel>, <User Martin>, <User Shyamli>]"

    def test_passwords(self):
        user1 = User('  Shyamli   ', 'pw12345')
        user2 = User('Martin', 'p90')
        assert str(user1) == "<User Shyamli>"
        assert str(user1.password) == "pw12345"
        assert str(user2) == "<User Martin>"
        assert user2.password is None


@pytest.fixture
def read_books_and_authors():
    books_file_name = 'comic_books_excerpt.json'
    authors_file_name = 'book_authors_excerpt.json'

    # we use a method from a utils file in the root folder to figure out the root
    # this way testing code is always finding the right path to the data files
    root_folder = get_project_root()
    data_folder = Path("library/adapters/data")
    path_to_books_file = str(root_folder / data_folder / books_file_name)
    path_to_authors_file = str(root_folder / data_folder / authors_file_name)
    reader = BooksJSONReader(path_to_books_file, path_to_authors_file)
    reader.read_json_files()
    return reader.dataset_of_books


class TestBooksJSONReader:

    def test_read_books_from_file(self, read_books_and_authors):
        dataset_of_books = read_books_and_authors
        assert str(dataset_of_books[0]) == "<Book The Switchblade Mamma, book id = 25742454>"
        assert str(dataset_of_books[9]) == "<Book War Stories, Volume 4, book id = 27036539>"
        assert str(dataset_of_books[19]) == "<Book D.Gray-man, Vol. 16: Blood & Chains, book id = 18955715>"

    def test_read_books_from_file_and_check_authors(self, read_books_and_authors):
        dataset_of_books = read_books_and_authors
        assert str(dataset_of_books[0].authors[0]) == "<Author Lindsey Schussman, author id = 8551671>"
        assert str(dataset_of_books[15].authors[0]) == "<Author Maki Minami, author id = 791996>"
        assert len(dataset_of_books[3].authors) == 2
        assert str(dataset_of_books[3].authors[1]) == "<Author Chris  Martin, author id = 853385>"

    def test_read_books_from_file_and_check_other_attributes(self, read_books_and_authors):
        dataset_of_books = read_books_and_authors
        assert dataset_of_books[2].release_year == 2012
        assert dataset_of_books[
                   19].description == "Lenalee is determined to confront a Level 4 Akuma that's out to kill Komui, but her only chance is to reclaim her Innocence and synchronize with it. The Level 4 is not inclined to wait around and pursues its mission even against the best efforts of Lavi and Kanda. It's left to Allen to hold the line, but it soon becomes obvious he has no hope of doing it all by himself!"
        assert str(dataset_of_books[4].publisher) == "<Publisher DC Comics>"
        assert isinstance(dataset_of_books[4].publisher, Publisher)
        assert isinstance(dataset_of_books[4].authors[0], Author)
        assert dataset_of_books[4].ebook is False
        assert dataset_of_books[0].ebook is True
        assert dataset_of_books[0].num_pages is None
        assert dataset_of_books[2].num_pages == 146
        assert dataset_of_books[5].num_pages == 206

    def test_read_books_from_file_special_characters(self, read_books_and_authors):
        dataset_of_books = read_books_and_authors
        assert dataset_of_books[17].title == "續．星守犬"
