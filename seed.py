"""
Generates some data for my Lending Library Flask app

Rollin S.
1/4/2024
"""

import random
import string
import secrets
import hashlib
from faker import Faker
from library.src import create_app
from library.src.models import db, Profile, Book, Author, Library, Review, Reader, libraries_readers_table, library_books_table, readers_books_table


# Constants
USERS_COUNT = 100
BOOKS_COUNT = 600
AUTHORS_COUNT = 90
LIBRARIES_COUNT = 10
REVIEWS_COUNT = 450
LIBRARY_STOCK = 600
CHECKED_OUT_BOOKS = 40





def random_passhash():
    """Get hashed and salted password of length N | 8 <= N <= 15"""
    raw = ''.join(
        random.choices(
            string.ascii_letters + string.digits + '!@#$%&', # valid pw characters
            k=random.randint(8, 15) # length of pw
        )
    )

    salt = secrets.token_hex(16)

    return hashlib.sha512((raw + salt).encode('utf-8')).hexdigest()


def truncate_tables():
    """Delete all rows from database tables"""
    db.session.execute(readers_books_table.delete())
    db.session.execute(libraries_readers_table.delete())
    db.session.execute(library_books_table.delete())
    
    Review.query.delete()
    Book.query.delete()
    Library.query.delete()
    Author.query.delete()
    Reader.query.delete()
    Profile.query.delete()
    
    db.session.commit()

def main():
    """Where the magic happens"""
    app = create_app()
    app.app_context().push()
    truncate_tables()
    faker = Faker()

    last_profile = None
    
    for _ in range(USERS_COUNT):
        last_profile = Profile(
            library_card = faker.unique.numerify(text='##########'),
            username = faker.unique.user_name(),
            password = random_passhash()
        )
        """last_reader = Reader(
            library_card = last_profile.library_card
        )"""
        db.session.add(last_profile)
        #db.session.add(last_reader)

    db.session.commit()

    last_reader = None
    for n in range(last_profile.id - USERS_COUNT + 1, last_profile.id):
        last_reader = Reader(
            library_card = n
        )
        db.session.add(last_reader)
    db.session.commit()

    last_author = None
    for _ in range(AUTHORS_COUNT):
        last_author = Author(
            name = faker.unique.name(),
            bio = faker.paragraph(nb_sentences=4)
        )
        db.session.add(last_author)
    db.session.commit()

    last_library = None
    for _ in range(LIBRARIES_COUNT):
        last_library = Library(
            branch_name=faker.city() + " Branch",
            location=faker.address()
        )
        db.session.add(last_library)
    db.session.commit()

    last_book = None
    for _ in range(BOOKS_COUNT):
        last_book = Book(
            title = faker.sentence(nb_words=3),
            genre = faker.word(ext_word_list=['fiction', 'sci-fi', 'fantasy', 'romance', 'cookbook', 'non-fiction', 'young adult', 'children\'s', 'mystery', 'thriller', 'horror', 'philosophy']),
            format=faker.word(ext_word_list=['paperback', 'hardback', 'ebook', 'audiobook']),
            publish_year= faker.year(),
            author = random.randint(last_author.id - AUTHORS_COUNT + 1, last_author.id)
        )
        db.session.add(last_book)
    db.session.commit()

    last_review = None
    for _ in range(REVIEWS_COUNT):
        last_review = Review(
            reviewer = random.randint(last_reader.id - USERS_COUNT + 2, last_reader.id),
            book_id = random.randint(last_book.id - BOOKS_COUNT + 1, last_book.id),
            review_body= faker.paragraph(),
            rating= random.randint(0,10)
        )
        db.session.add(last_review)
    db.session.commit()

    library_stock_pairs = set()
    while len(library_stock_pairs) < LIBRARY_STOCK:
        candidate = (
            random.randint(last_library.id - LIBRARIES_COUNT +1, last_library.id),
            random.randint(last_book.id - BOOKS_COUNT + 1, last_book.id)
        )
        if candidate in library_stock_pairs:
            continue
        
        library_stock_pairs.add(candidate)


    new_stock = [{"library_id": pair[0], "book_id": pair[1], "copies": random.randint(1,10), "available_copies": random.randint(0,10)} for pair in list(library_stock_pairs)]
    insert_stock_query = library_books_table.insert().values(new_stock)
    db.session.execute(insert_stock_query)
    db.session.commit()

    library_readers_pairs = set()
    while len(library_readers_pairs) < USERS_COUNT * 0.25:
        candidate = (
            random.randint(last_library.id - LIBRARIES_COUNT + 1, last_library.id),
            random.randint(last_reader.id - USERS_COUNT + 1, last_reader.id)
        )
        if candidate in library_readers_pairs:
            continue
        library_readers_pairs.add(candidate)

    new_lender = [{"library_id": pair[0], "reader_id": pair[1]} for pair in list(library_readers_pairs)]
    insert_lender_query = libraries_readers_table.insert().values(new_lender)
    db.session.execute(insert_lender_query)
    db.session.commit()

    readers_books_pairs = set()
    while len(readers_books_pairs) < CHECKED_OUT_BOOKS:
        candidate = (
            random.randint(last_reader.id - USERS_COUNT + 1, last_reader.id),
            random.randint(last_book.id - BOOKS_COUNT + 1, last_book.id)
        )
        if candidate in readers_books_pairs:
            continue
        readers_books_pairs.add(candidate)

    new_reader = [{"reader_id": pair[0], "book_id": pair[1], "checked_out": faker.date_this_year(), "due_date": faker.date_this_year(after_today=True)} for pair in list(readers_books_pairs)]
    insert_reader_query = readers_books_table.insert().values(new_reader)
    db.session.execute(insert_reader_query)
    db.session.commit()

main()