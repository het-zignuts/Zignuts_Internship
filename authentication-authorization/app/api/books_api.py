from fastapi import APIRouter, HTTPException, Query, Depends
from uuid import UUID, uuid4
from typing import List, Optional
from app.schema.schemas.book import BookCreate, BookUpdate, BookResponse, BookPatch
from app.auth.deps import get_current_user, check_book_owner_or_admin
from app.models.user import User
from app.models.book import Book
from app.crud.book import create_book, get_book, update_book, delete_book, partial_update_book, get_books
from app.db.session import DatabaseSession
from sqlmodel import Session

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=BookResponse)
def api_create_book(book: BookCreate, session: Session = Depends(DatabaseSession().get_session), current_user: User = Depends(get_current_user)):
    book_created = create_book(book, session, current_user)
    if book_created is None:
        raise HTTPException(status_code=400, detail="Book could not be created")
    return book_created

@router.get("/{book_id}", response_model=BookResponse)
def api_get_book(book_id: UUID, session: Session = Depends(DatabaseSession().get_session), current_user: User = Depends(get_current_user)):
    book = get_book(book_id, session)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if check_book_owner_or_admin(book, current_user):
        return book
    raise HTTPException(status_code=403, detail="Insufficient permissions")

@router.put("/{book_id}", response_model=BookResponse)
def api_update_book(book_id: UUID, new_book: BookUpdate, session: Session = Depends(DatabaseSession().get_session), current_user: User = Depends(get_current_user)):
    book = update_book(book_id, new_book, session)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if check_book_owner_or_admin(book, current_user):
        return book
    raise HTTPException(status_code=403, detail="Insufficient permissions")

@router.delete("/{book_id}", response_model=dict)
def api_delete_book(book_id: UUID, session: Session = Depends(DatabaseSession().get_session), current_user: User = Depends(get_current_user)):
    book = get_book(book_id, session)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if check_book_owner_or_admin(book, current_user):
        book_deleted = delete_book(book_id, session)
        if not book_deleted:
            raise HTTPException(status_code=404, detail="Book not found")
        return {"detail": "Book deleted successfully"}
    raise HTTPException(status_code=403, detail="Insufficient permissions")

@router.get("/", response_model=List[BookResponse])
def api_list_books(author: str = Query(default=None, max_length=100), session: Session = Depends(DatabaseSession().get_session), current_user: User = Depends(get_current_user)):
        books = get_books(session, author)
        if not books:
            raise HTTPException(status_code=404, detail="No books found")
        return books

@router.patch("/{book_id}", response_model=BookResponse)
def api_partial_update_book(book_id: UUID, new_book: BookPatch, session: Session = Depends(DatabaseSession().get_session), current_user: User = Depends(get_current_user)):
    book = partial_update_book(book_id, new_book, session)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if check_book_owner_or_admin(book, current_user):
        return book
    raise HTTPException(status_code=403, detail="Insufficient permissions")
