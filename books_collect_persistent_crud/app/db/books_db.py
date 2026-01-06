from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4

class Book(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(max_length=200)
    author: str = Field(max_length=100)
    isbn: str = Field(max_length=13, unique=True)
    publication_year: int = Field(ge=0)