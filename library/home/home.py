from flask import Blueprint, render_template

from library.utilities import utilities

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template(
        'home/home.html',
        selected_books=utilities.get_selected_books(12)
    )
