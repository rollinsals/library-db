"""
Models for Library DB Project

Rollin Salsbery
"""

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


library_books_table = db.Table(
    'libraries_books',
    db.Column(
        'library_id', db.Integer,
        db.ForeignKey('libraries.id'),
        primary_key=True
    ),
    db.Column(
        'book_id', db.Integer,
        db.ForeignKey('books.id'),
        primary_key=True
    ),
    db.Column(
        'copies', db.Integer,
        nullable=False
    ),
    db.Column(
        'available_copies', db.Integer,
        nullable=False
    )
)

readers_books_table = db.Table(
    'readers_books',
    db.Column(
        'book_id', db.Integer,
        db.ForeignKey('books.id'),
        primary_key=True
    ),
    db.Column(
        'reader_id', db.Integer,
        db.ForeignKey('readers.id'),
        primary_key=True
    ),
    db.Column(
        'checked_out', db.Date,
        default=datetime.date.today,
        nullable=False
    ),
    db.Column(
        'due_date', db.Date,
        default=datetime.date.today() + datetime.timedelta(days=21),
        nullable=False
    )
)

# I am not actually sure this table is actually needed. 
# Since I didn't get to implementing loans fully, it's hard to tell
libraries_readers_table = db.Table(
    'libraries_readers',
    db.Column(
        'library_id', db.Integer,
        db.ForeignKey('libraries.id'),
        primary_key=True
    ),
    db.Column(
        'reader_id', db.Integer,
        db.ForeignKey('readers.id'),
        primary_key=True
    )
)


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String)
    genre = db.Column(db.String)
    format = db.Column(db.String)
    publish_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    libraries_available = db.relationship('Library',secondary=library_books_table, lazy='subquery', backref=db.backref('books', lazy=True))
    book_reviews = db.relationship('Review', backref='book')

    def __init__(self, title: str, genre: str, book_format: str, publish_year: int, author: int):
        self.title = title
        self.genre = genre
        self.format = book_format
        self.publish_year = publish_year
        self.author_id = author
    
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'author_id': self.author_id,
            'genre': self.genre,
            'format': self.format,
            'publish_year': self.publish_year
        }
   
class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String, nullable=False)
    bio = db.Column(db.String)
    # backref to list of books written
    books_written = db.relationship('Book', backref='author')
    
    def __init__(self, name: str, bio: str):
        self.name = name
        self.bio = bio

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'bio': self.bio
        }
   
class Library(db.Model):
    __tablename__ = 'libraries'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    branch_name = db.Column(db.String)
    location = db.Column(db.String)

    
    # access the books-libraries list so I can get the copies there (somehow?)
    inv_books = db.relationship('Book', secondary=library_books_table, lazy='subquery', backref=db.backref('libraries', lazy=True))
    current_readers = db.relationship('Reader', secondary=libraries_readers_table, lazy='subquery', backref=db.backref('libraries', lazy=True))

    def __init__(self, branch_name: str, location: str):
        self.branch_name = branch_name
        self.location = location
    
    def serialize(self):
        return {
            'id': self.id,
            'branch_name': self.branch_name,
            'location': self.location

        }

class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    library_card = db.Column(db.String(10), unique= True, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self,library_card: str, username: str, password: str):
        self.library_card = int(library_card)
        self.username = username
        self.password = password

    def serialize(self):
        return {
            'id': self.id,
            'library card': self.library_card,
            'username': self.username
        }



class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    review_body = db.Column(db.String)
    rating = db.Column(db.Integer)
    reviewer= db.Column(db.Integer, db.ForeignKey('readers.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)

    

    def __init__(self, reviewer, book_id, review_body, rating):
        self.reviewer = reviewer
        self.book_id = book_id
        self.review_body = review_body
        self.rating = rating

    def serialize(self):
        return {
            'reviewer': self.reviewer,
            'book id': self.book_id,
            'review_body': self.review_body,
            'rating': self.rating
        }



class Reader(db.Model):
    __tablename__ = 'readers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    library_card = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    reviews = db.relationship('Review', backref='reader', cascade="all,delete")
    # backref to user in order to get username, etc.
    # backref to books
    books_checked_out = db.relationship(
        'Book', secondary=readers_books_table,
        lazy='subquery',
        backref=db.backref('reader', lazy=True)
    )
    libraries_under = db.relationship('Library', secondary=libraries_readers_table, backref=db.backref('reader', lazy=True))

