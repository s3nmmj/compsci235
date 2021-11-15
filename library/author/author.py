from flask import Blueprint, render_template, request, url_for

import library.adapters.repository as repo

import library.author.services as services
from library.utilities import utilities

author_blueprint = Blueprint(
    'author_bp', __name__)


@author_blueprint.route('/authors', methods=['GET'])
def author_list():
    cursor = request.args.get('cursor')
    next_authors_url = None
    prev_authors_url = None

    if cursor is None:
        cursor = 0
    else:
        cursor = int(cursor)

    if cursor > 0:
        prev_authors_url = url_for('author_bp.author_list', cursor=cursor - 1)
    if (cursor + 1) * services.default_page_size < services.get_number_of_authors(repo.repo_instance):
        next_authors_url = url_for('author_bp.author_list', cursor=cursor + 1)

    return render_template(
        'author/author.html',
        selected_authors=services.get_authors(repo.repo_instance, cursor),
        prev_authors_url=prev_authors_url,
        next_authors_url=next_authors_url
    )
