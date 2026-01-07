from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from app.core.security import UserRole

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    email: str = Field(max_length=100, nullable=False, unique=True)
    password: str = Field(max_length=100, nullable=False)
    role: UserRole = Field(default=UserRole.USER, max_length=10, nullable=False)
    books: list["Book"] = Relationship(back_populates="owner", cascade="all, delete-orphan")
