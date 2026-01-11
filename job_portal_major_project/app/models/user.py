from sqlmodel import SQLModel, Field
from typing import Optional
from app.core.enum import UserRole
from datetime import datetime, timezone
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_name: str = Field(index=True, unique=True, nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    password: str = Field(nullable=False)
    role: UserRole = Field(default=UserRole.CANDIDATE, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Optional[datetime] = Field(default=None, nullable=True)
    current_organization: Optional[UUID] = Field(default=None, nullable=True, foreign_key="company.id")