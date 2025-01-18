from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.models.book import Book
from app.schemas.book import BookCreate, Book as BookSchema, PaginatedBooks
from app.api.v1.endpoints.auth import get_current_user
from app.core.errors import NotFoundError, ValidationError
from sse_starlette.sse import EventSourceResponse
import json
import uuid
from app.core.events import get_book_update_queue, remove_client, send_book_update
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/stream", 
    summary="Stream book updates",
    description="SSE endpoint for real-time book updates")
async def stream_book_updates(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    client_id = str(uuid.uuid4())
    
    async def event_generator():
        queue = await get_book_update_queue(client_id)
        try:
            # Send initial connection event
            yield {
                "event": "connected",
                "data": json.dumps({
                    "status": "connected", 
                    "client_id": client_id
                })
            }
            
            while True:
                message = await queue.get()
                if message is None:
                    break
                yield {
                    "event": message["event"],
                    "data": json.dumps(message)
                }
        except Exception:
            pass
        finally:
            await remove_client(client_id, background_tasks)
    
    return EventSourceResponse(event_generator())

@router.post("/", 
    response_model=BookSchema,
    summary="Create a new book",
    description="Create a new book in the database")
async def create_book(
    book: BookCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    
    book_data = {
        "id": db_book.id,
        "title": db_book.title,
        "author": db_book.author,
        "published_date": db_book.published_date,
        "summary": db_book.summary,
        "genre": db_book.genre
    }
    
    # Send update event
    await send_book_update("created", db_book.id, book_data)
    return db_book

@router.get("/{book_id}", 
    response_model=BookSchema,
    summary="Get a specific book",
    description="Retrieve a book by its ID")
def get_book(
    book_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise NotFoundError("Book")
    return db_book

@router.get("/", 
    response_model=PaginatedBooks,
    summary="Get all books",
    description="Retrieve all books with pagination support")
def get_books(
    page: int = Query(1, ge=1, description="Page number for pagination"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    items_per_page = 50
    total = db.query(Book).count()
    logger.info(f"Total books in DB: {total}")
    
    total_pages = (total + items_per_page - 1) // items_per_page
    logger.info(f"Total pages: {total_pages}")
    
    skip = (page - 1) * items_per_page
    logger.info(f"Skipping {skip} items")
    
    books = db.query(Book).offset(skip).limit(items_per_page).all()
    logger.info(f"Retrieved {len(books)} books")
    
    result = {
        "total": total,
        "items": books,
        "page": page,
        "pages": total_pages
    }
    logger.info(f"Result length: {len(result['items'])}")
    return result

@router.put("/{book_id}", 
    response_model=BookSchema,
    summary="Update a book",
    description="Update an existing book's details")
async def update_book(
    book_id: int,
    book: BookCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise NotFoundError("Book")
    
    for key, value in book.model_dump().items():
        setattr(db_book, key, value)
    
    db.commit()
    db.refresh(db_book)
    
    # Send update event
    await send_book_update("updated", db_book.id, db_book.__dict__)
    return db_book

@router.delete("/{book_id}",
    summary="Delete a book",
    description="Delete a book from the database")
async def delete_book(
    book_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise NotFoundError("Book")
    
    db.delete(db_book)
    db.commit()
    
    # Send update event
    await send_book_update("deleted", book_id)
    return {"message": "Book deleted successfully"}