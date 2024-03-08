

from flask import Blueprint, jsonify, abort, request
from ..models import Reader, Profile, Book, Library, readers_books_table, db
import sqlalchemy


bp = Blueprint('readers', __name__, url_prefix='/user')
@bp.route('', methods=['GET'])
def index():
    readers = Reader.query.all()
    result = []
    for r in readers:
        result.append(r.serialize())
    return jsonify(result)

@bp.route('<int:id>', methods=['GET'])
def show(id: int):
    reader = Reader.query.get_or_404(id, "User not found")
    acct = Profile.query.get(reader.library_card)
    return jsonify(acct.serialize())

@bp.route('/<int:id>/reviews', methods=['GET'])
def show_reviews(id: int):
    reader = Reader.query.get_or_404(id, "Account not found")
    result = []
    for r in reader.reviews:
        result.append(r.serialize())
    return jsonify(result)

@bp.route('/<int:id>/loans', methods=['GET'])
def show_loans(id: int):
    reader = Reader.query.get_or_404(id, "Account not found")
    result = []
    for b in reader.books_checked_out:
        result.append(b.serialize())
    return jsonify(result)

@bp.route('', methods=['POST'])
def check_out():
    """
    Adds book to relationship of books/readers. 
    Perhaps better to put this under books API? I have no idea how the front end would be
    """
    
    if "reader_id" not in request.json or "book_id" not in request.json: # or "library_id" not in request.json:
        abort(400)
    r = Reader.query.get_or_404(request.json["reader_id"], "User not found")
    b = Book.query.get_or_404(request.json["book_id"], "Book not found")
    #l = Library.query.get_or_404(request.json["library_id", "Branch not found"])

    # if library_books_table contains (l,b) -> is available copies > 0? update available copies
    # else return false

    stmt = sqlalchemy.insert(readers_books_table).values(book_id = b.id, reader_id = r.id)

    try:
        db.session.execute(stmt)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)
    

@bp.route('/<int:id>/loans', methods=['DELETE'])
def return_book(id: int):
    if 'book_id' not in request.json:
        abort(400)
    r = Reader.query.get_or_404(id, "User not found")
    b = Book.query.get_or_404(request.json['book_id'])

    stmt = sqlalchemy.delete(readers_books_table).where(readers_books_table.c.reader_id == r.id and readers_books_table.c.book_id == b.id)
    try:
        db.session.execute(stmt)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)