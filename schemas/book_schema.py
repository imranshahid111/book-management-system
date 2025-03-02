from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    price: float
    publication_year: int

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    price: float
    publication_year: int