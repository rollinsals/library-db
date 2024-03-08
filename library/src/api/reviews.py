

from flask import Blueprint, jsonify, abort, request
from ..models import Review, Reader, Book, db

bp = Blueprint('reviews', __name__, url_prefix='/reviews')

# show all
@bp.route('', methods=['GET'])
def index():
    reviews = Review.query.all()
    result = []
    for rev in reviews:
        result.append(rev.serialize())
    return jsonify(result)

# show
@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    review = Review.query.get_or_404(id, "Review not found")
    return jsonify(review.serialize())

# create new review
@bp.route('', methods=['POST'])
def create():
    if "reader_id" not in request.json or "book_id" not in request.json or "review_body" not in request.json and "rating" not in request.json:
        abort(400)
    reader = Reader.query.get_or_404(request.json["reader_id"], "User not found")
    book = Book.query.get_or_404(request.json["book_id"], "Book not found")

    body = ""
    rate = None
    if "review_body" in request.json:
        body = request.json["review_body"]
    if "rating" in request.json:
        rate = request.json["rating"]

    rev = Review(
        reviewer = request.json["reader_id"],
        book_id = request.json["book_id"],
        review_body = body,
        rating = rate
    )
    db.session.add(rev)
    db.session.commit()
    return jsonify(rev.serialize())

# update body text and/or rating
@bp.route('<int:id>', methods=['PUT', 'PATCH'])
def update(id: int):
    if "review_body" not in request.json and "rating" not in request.json:
        abort(400)
    rev = Review.query.get_or_404(id, "Review not found")

    if "review_body" in request.json:
        rev.review_body = request.json["review_body"]
    if "rating" in request.json:
        rev.rating = request.json["rating"]

    try:
        db.session.commit()
        return jsonify(True, rev.serialize())
    except:
        return jsonify(False)

# delete
@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    """Removes review"""
    rev = Review.query.get_or_404(id, "Review not found")
    try:
        db.session.delete(rev)
        db.sesson.commit()
        return jsonify(True)
    except:
        return jsonify(False)