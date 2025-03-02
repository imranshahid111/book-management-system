from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.book import Book
from database import SessionLocal

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/books/")
def read_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books