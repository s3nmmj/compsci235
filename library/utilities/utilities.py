# Configure Blueprint.
from flask import Blueprint, url_for

import library.adapters.repository as repo
import library.utilities.services as services

utilities_blueprint = Blueprint('utilities_bp', __name__)


def get_selected_books(quantity=6):
    books = services.get_random_books(quantity, repo.repo_instance)

    return books
