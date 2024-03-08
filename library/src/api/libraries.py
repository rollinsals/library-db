"""
Oh god
"""

from flask import Blueprint, jsonify, abort, request
from ..models import Library, db

bp = Blueprint('libraries', __name__, url_prefix='/branches')

# show all
@bp.route('', methods=['GET'])
def index():
    branches = Library.query.all()
    result = []
    for b in branches:
        result.append(b.serialize())
    return jsonify(result)

# show
@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    branch = Library.query.get_or_404(id, "Branch not found")
    return jsonify(branch.serialize())

# show the books associated with this library
# not sure how to access the copies columns in the intermediate table
@bp.route('/<int:id>/book_inventory', methods=['GET'])
def list_books(id: int):
    branch = Library.query.get_or_404(id, "Branch not found")
    result = []
    for b in branch.inv_books:
        result.append(b.serialize())
    return jsonify(result)

