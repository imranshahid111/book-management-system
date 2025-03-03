from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from models.book import Book
from database import SessionLocal

router = APIRouter()

templates = Jinja2Templates(directory="templates")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Home page - List all books
@router.get("/", response_class=HTMLResponse)
async def list_books(request: Request, db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return templates.TemplateResponse("list_books.html", {"request": request, "books": books})

# Add book page
@router.get("/add", response_class=HTMLResponse)
async def add_book_page(request: Request):
    return templates.TemplateResponse("add_book.html", {"request": request})

# Handle add book form submission
@router.post("/add")
async def add_book(
    title: str = Form(...),
    author: str = Form(...),
    genre: str = Form(...),
    price: float = Form(...),
    publication_year: int = Form(...),
    db: Session = Depends(get_db)
):
    book = Book(title=title, author=author, genre=genre, price=price, publication_year=publication_year)
    db.add(book)
    db.commit()
    db.refresh(book)
    return RedirectResponse(url="/", status_code=303)

# Edit book page
@router.get("/edit/{book_id}", response_class=HTMLResponse)
async def edit_book_page(request: Request, book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return templates.TemplateResponse("edit_book.html", {"request": request, "book": book})

# Handle edit book form submission
@router.post("/edit/{book_id}")
async def edit_book(
    book_id: int,
    title: str = Form(...),
    author: str = Form(...),
    genre: str = Form(...),
    price: float = Form(...),
    publication_year: int = Form(...),
    db: Session = Depends(get_db)
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.title = title
    book.author = author
    book.genre = genre
    book.price = price
    book.publication_year = publication_year
    db.commit()
    return RedirectResponse(url="/", status_code=303)

# Delete book
@router.get("/delete/{book_id}")
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return RedirectResponse(url="/", status_code=303)
