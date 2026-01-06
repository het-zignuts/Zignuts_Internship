from typing import List, Optional
from sqlmodel import Session, select
from app.schema.books_schema import BookCreate, BookResponse, BookUpdate, BookPatch
from app.db.books_db import Book

def create_book(book: BookCreate, session: Session) -> BookResponse:
    book=Book(**book.model_dump())
    session.add(book)
    session.commit()
    session.refresh(book)

    return BookResponse(**book.model_dump())
    
def get_book(book_id: UUID, session: Session) -> Optional[BookResponse]:
    book=session.get(Book, book_id)
    if book:
        return BookResponse(**book.model_dump())
    return None

def get_books(session: Session, author: Optional[str] = None) -> List[BookResponse]:
    query = select(Book)
    if author:
        query = query.where(Book.author == author)
    books = session.exec(query).all()
    return [BookResponse(**book.model_dump()) for book in books]

def partial_update_book(book_id: UUID, new_book: BookPatch, session: Session) -> Optional[BookResponse]:
    book=session.get(Book, book_id)
    if not book:
        return None

    book_data=new_book.model_dump(exclude_unset=True)

    for key, value in book_data.items():
        setattr(book, key, value)
    session.add(book)
    session.commit()
    session.refresh(book)

    return BookResponse(**book.model_dump())

def update_book(book_id: UUID, new_book: BookUpdate, session: Session) -> Optional[BookResponse]:
    book=session.get(Book, book_id)
    if not book:
        return None

    book_data=new_book.model_dump()

    for key, value in book_data.items():
        setattr(book, key, value)
    session.add(book)
    session.commit()
    session.refresh(book)

    return BookResponse(**book.model_dump())

def delete_book(book_id: UUID, session: Session) -> bool:
    book=session.get(Book, book_id)
    if not book:
        return False
    session.delete(book)
    session.commit()
    return True