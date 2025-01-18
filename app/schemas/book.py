from datetime import date
from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    published_date: str
    summary: str
    genre: str

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        from_attributes = True

class PaginatedBooks(BaseModel):
    total: int
    items: list[Book]
    page: int
    pages: int