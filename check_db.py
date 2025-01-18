from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Create engine
engine = create_engine('sqlite:///app/db/books.db')
Session = sessionmaker(bind=engine)
session = Session()

try:
    # Count books
    count = session.execute(text('SELECT COUNT(*) FROM books')).scalar()
    print(f"Total books: {count}")

    # Get some sample data
    books = session.execute(text('SELECT * FROM books LIMIT 5')).fetchall()
    print("\nSample books:")
    for book in books:
        print(book)
finally:
    session.close()