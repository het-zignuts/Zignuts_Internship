from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped

if TYPE_CHECKING:
    from .user import User  # to avoid circular import at runtime

class Book(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    title: str = Field(max_length=100, nullable=False, unique=True)
    author: str = Field(max_length=100, nullable=False)
    publication_year: int | None = Field(default=None, nullable=True)
    isbn: str | None = Field(default=None, max_length=13, nullable=True, unique=True)
    owner_id: UUID = Field(foreign_key="user.id", nullable=False,)
    owner: Mapped[Optional["User"]] = Relationship(back_populates="books")