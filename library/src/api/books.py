

from flask import Blueprint, jsonify, abort, request
from ..models import Book, db
import sqlalchemy

bp = Blueprint('books', __name__, url_prefix='/books')

# index
@bp.route("", methods=['GET'])
def index():
    books = Book.query.all()
    result = []
    for b in books:
        result.append(b.serialize())
    return jsonify(result)
# show
@bp.route("/<int:id>", methods=['GET'])
def show(id:int):
    book = Book.query.get_or_404(id, "Book not found")
    return jsonify(book.serialize())
# create new book
@bp.route("", methods=['POST'])
def create():
    if "title" not in request.json or "author_id" not in request.json:
        abort(400)

    new_genre = None
    if 'genre' in request.json:
        new_genre = request.json["genre"]

    new_format = None
    if 'format' in request.json:
        new_format = request.json["format"]

    new_pub = None
    if 'publish_year' in request.json:
        new_pub = request.json["publish_year"]

    b = Book(
        title=request.json["title"],
        genre=new_genre,
        format=new_format,
        publish_year=new_pub,
        author=request.json["author_id"]
    )
    db.session.add(b)
    db.session.commit()
    return jsonify(b.serialize())
# delete book
@bp.route("/<int:id>", methods=['DELETE'])
def delete(id: index):
    b = Book.query.get_or_404(id, "Book not found")
    try:
        db.session.delete(b)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)
# list libraries with copies of this book
@bp.route("<int:id>/libraries", methods=['GET'])
def show_libraries_available(id: int):
    b = Book.query.get_or_404(id, "Book not found")
    results = []
    for l in b.libraries_available:
        results.append(l.serialize())
    return jsonify(results)

@bp.route('<int:id>/reviews', methods=['GET'])
def show_book_reviews(id: int):
    book = Book.query.get_or_404(id, "Book not found")
    result = []
    for rev in book.book_reviews:
        result.append(rev.serialize())
    
    return jsonify(result)

@bp.route('<int:id>/reviews/avg', methods=['GET'])
def show_avg_rating(id: int):
    book = Book.query.get_or_404(id, "Book not found")
    rating_total = 0
    count = 0
    for rev in book.book_reviews:
        if rev.rating is not None:
            rating_total += rev.rating
            count += 1
    avg = rating_total/count
        
    return jsonify({"Average Rating": avg})