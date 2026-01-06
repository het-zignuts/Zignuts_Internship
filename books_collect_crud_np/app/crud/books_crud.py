from typing import List, Optional
from uuid import UUID, uuid4
from app.schema.books_schema import BookCreate, BookUpdate, BookResponse, BookPatch
from app.db.books_db import books_db

def create_book(book: BookCreate) -> BookResponse:
    new_book = {
        "id": uuid4(),
        "title": book.title,
        "author": book.author,
        "isbn": book.isbn,
        "publication_year": book.publication_year
    }
    books_db.append(new_book)
    return BookResponse(**new_book)

def get_book(book_id: UUID) -> Optional[BookResponse]:
    for book in books_db:
        if book["id"] == book_id:
            return BookResponse(**book)
    return None

def get_books(author: Optional[str] = None) -> List[BookResponse]:
    books=[]
    if author:
        for book in books_db:
            if book["author"] == author:
                books.append(BookResponse(**book))
    else:
        for book in books_db:
            books.append(BookResponse(**book))
    return books

def partial_update_book(book_id: UUID, new_book: BookPatch) -> Optional[BookResponse]:
    for book in books_db:
        if book["id"] == book_id:
            if new_book.title is not None:
                book["title"] = new_book.title
            if new_book.author is not None:
                book["author"] = new_book.author
            if new_book.isbn is not None:
                book["isbn"] = new_book.isbn
            if new_book.publication_year is not None:
                book["publication_year"] = new_book.publication_year
            return BookResponse(**book)
    return None

def update_book(book_id: UUID, new_book: BookUpdate) -> Optional[BookResponse]:
    for book in books_db:
        if book["id"] == book_id:
            book["title"] = new_book.title
            book["author"] = new_book.author
            book["isbn"] = new_book.isbn
            book["publication_year"] = new_book.publication_year
            return BookResponse(**book)
    return None

def delete_book(book_id: UUID) -> bool:
    for index, book in enumerate(books_db):
        if book["id"] == book_id:
            del books_db[index]
            return True
    return False