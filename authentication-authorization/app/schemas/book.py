from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class BookCreate(BaseModel):
    title: str = Field(max_length=200)
    author: str = Field(max_length=100)
    isbn: Optional[str] = Field(max_length=10)
    publication_year: Optional[int] = Field(ge=0)
    owner_id: UUID

class BookUpdate(BaseModel):
    title: str 
    author: str
    isbn: Optional[str] = Field(default=None, max_length=10)
    publication_year: Optional[int] = Field(default=None, ge=0)

class BookPatch(BaseModel):
    title: Optional[str] = Field(default=None, max_length=200)
    author: Optional[str] = Field(default=None, max_length=100)
    isbn: Optional[str] = Field(default=None, max_length=10)
    publication_year: Optional[int] = Field(default=None, ge=0)

class BookResponse(BaseModel):
    id: UUID
    title: str
    author: str
    isbn: Optional[str]
    publication_year: Optional[int]
    owner_id: UUID