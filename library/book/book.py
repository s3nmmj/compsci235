from better_profanity import profanity
from flask import Blueprint, render_template, request, url_for, session, redirect
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, ValidationError

import library.adapters.repository as repo
import library.book.services as services
from library.authentication.authentication import login_required
from library.domain.model import ShelfName
from library.utilities import utilities

book_blueprint = Blueprint(
    'book_bp', __name__)


@book_blueprint.route('/books', methods=['GET'])
def book_list():
    selected_books = []
    next_authors_url = None
    prev_authors_url = None
    # Read query parameters.
    search_type = request.args.get('search_type')
    if search_type == 'book':
        book_id = request.args.get('book_id')
        if book_id:
            selected_book = services.get_book_by_id(repo.repo_instance, int(book_id))

            if selected_book:
                form = ReviewForm(book_id=selected_book.book_id)
                reading_list_form = ReadingListForm(book_id=selected_book.book_id)
                # Store the article id in the form.
                form.book_id.data = selected_book.book_id
                reviews = services.get_reviews_by_book_id(repo.repo_instance, int(book_id))
                return render_template(
                    'book/book_detail.html',
                    selected_book=selected_book,
                    recommended_books=utilities.get_selected_books(8),
                    display_review_input=request.args.get('display_review_input'),
                    handler_url=url_for('book_bp.review_on_book'),
                    reading_list_handler_url=url_for('book_bp.my_books'),
                    display_shelf_input=request.args.get('display_shelf_input'),
                    form=form,
                    reading_list_form=reading_list_form,
                    reviews=reviews
                )
    elif search_type == 'author':
        author_id = request.args.get('author_id')
        if author_id:
            selected_books = services.get_books_by_author_id(repo.repo_instance, int(author_id))
            recommended_books = utilities.get_selected_books(8)
    elif search_type == 'publisher':
        publisher_name = request.args.get('publisher_name')
        if publisher_name:
            selected_books = services.get_books_by_publisher(repo.repo_instance, publisher_name)
            recommended_books = utilities.get_selected_books(8)
    elif search_type == 'release_year':
        release_year = request.args.get('release_year')
        if release_year:
            selected_books = services.get_books_by_release_year(repo.repo_instance, int(release_year))
            recommended_books = utilities.get_selected_books(8)
    else:
        cursor = request.args.get('cursor')
        if cursor is None:
            cursor = 0
        else:
            cursor = int(cursor)

        if cursor > 0:
            prev_authors_url = url_for('book_bp.book_list', cursor=cursor - 1)
        if (cursor + 1) * services.default_page_size < services.get_number_of_books(repo.repo_instance):
            next_authors_url = url_for('book_bp.book_list', cursor=cursor + 1)
        selected_books = services.get_books(repo.repo_instance, cursor)

    if selected_books is None or selected_books == []:
        return render_template(
            'not_found.html',
            recommended_books=utilities.get_selected_books(8)
        )
    else:
        return render_template(
            'book/book.html',
            selected_books=selected_books,
            prev_authors_url=prev_authors_url,
            next_authors_url=next_authors_url,
            display_review_input=0
        )


@book_blueprint.route('/my_books', methods=['GET', 'POST'])
@login_required
def my_books():
    # Obtain the user name of the currently logged in user.
    user_name = session['user_name']
    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an book id, when subsequently called with a HTTP POST request, the book id remains in the
    # form.
    form = ReadingListForm()
    if form.validate_on_submit():
        book_id = int(form.book_id.data)
        # Use the service layer to store the book.
        services.add_book_to_user(user_name, book_id, form.reading_list.data, repo.repo_instance)

        return redirect(url_for('book_bp.book_list', book_id=book_id, search_type='book'))

    shelf = request.args.get('shelf')
    shelf_tag = shelf
    if shelf is None or shelf == 'current':
        shelf = ShelfName.CURRENTLY_READING
        shelf_tag = 'current'
    elif shelf == 'want':
        shelf = ShelfName.WANT_TO_READ
    elif shelf == 'read':
        shelf = ShelfName.READ
    else:
        return render_template(
            'not_found.html',
            recommended_books=utilities.get_selected_books(8)
        )

    selected_books = services.get_books_by_user_and_shelf(repo.repo_instance, user_name, shelf)

    return render_template(
        'book/my_books.html',
        shelf=shelf_tag,
        selected_books=selected_books,
        recommended_books=utilities.get_selected_books(8)
    )


@book_blueprint.route('/review', methods=['POST'])
@login_required
def review_on_book():
    # Obtain the user name of the currently logged in user.
    user_name = session['user_name']
    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an book id, when subsequently called with a HTTP POST request, the book id remains in the
    # form.
    form = ReviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the review text has passed data validation.
        # Extract the book id, representing the reviewed book, from the form.
        book_id = int(form.book_id.data)

        # Use the service layer to store the new review.
        services.add_review(book_id, form.review.data, user_name, repo.repo_instance)

        # Cause the web browser to display the page of all books that have the same date as the reviewed book,
        # and display all reviews, including the new review.
        return redirect(url_for('book_bp.book_list', book_id=book_id, search_type='book'))


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])

    book_id = HiddenField("Book id")
    submit = SubmitField('Submit')


class ReadingListForm(FlaskForm):
    reading_list = RadioField('Reading List', choices=[(ShelfName.WANT_TO_READ, ShelfName.WANT_TO_READ),
                                                       (ShelfName.CURRENTLY_READING, ShelfName.CURRENTLY_READING),
                                                       (ShelfName.READ, ShelfName.READ)],
                              default=ShelfName.WANT_TO_READ)
    book_id = HiddenField("Book id")
    submit = SubmitField('Add')
