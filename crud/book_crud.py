from sqlalchemy.orm import Session
from models.book import Book

def get_books(db: Session):
    return db.query(Book).all()

def create_book(db: Session, book_data: dict):
    book = Book(**book_data)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book