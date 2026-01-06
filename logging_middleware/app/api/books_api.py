from fastapi import APIRouter, HTTPException, Query, Depends
from uuid import UUID, uuid4
from typing import List, Optional
from app.schema.books_schema import BookCreate, BookUpdate, BookResponse, BookPatch
from app.crud.books_crud import create_book, get_book, update_book, delete_book, partial_update_book, get_books
from app.db.session import get_session
from sqlmodel import Session
from app.db.books_db import Book

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=BookResponse)
def api_create_book(book: BookCreate, session: Session = Depends(get_session)):
    book_created = create_book(book, session)
    if book_created is None:
        raise HTTPException(status_code=400, detail="Book could not be created")
    return book_created

@router.get("/{book_id}", response_model=BookResponse)
def api_get_book(book_id: UUID, session: Session = Depends(get_session)):
    book = get_book(book_id, session)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=BookResponse)
def api_update_book(book_id: UUID, new_book: BookUpdate, session: Session = Depends(get_session)):
    book = update_book(book_id, new_book, session)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.delete("/{book_id}", response_model=dict)
def api_delete_book(book_id: UUID, session: Session = Depends(get_session)):
    book_deleted = delete_book(book_id, session)
    if not book_deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"detail": "Book deleted successfully"}

@router.get("/", response_model=List[BookResponse])
def api_list_books(author: str = Query(default=None, max_length=100), session: Session = Depends(get_session)):
    books = get_books(session, author)
    if not books:
        raise HTTPException(status_code=404, detail="No books found")
    return books

@router.patch("/{book_id}", response_model=BookResponse)
def api_partial_update_book(book_id: UUID, new_book: BookPatch, session: Session = Depends(get_session)):
    book = partial_update_book(book_id, new_book, session)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

