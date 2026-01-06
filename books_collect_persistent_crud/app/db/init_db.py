from sqlmodel import SQLModel
from app.db.session import engine
from app.db.books_db import Book

def init_db():
    SQLModel.metadata.create_all(engine)