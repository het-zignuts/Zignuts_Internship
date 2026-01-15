from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from app.core.enum import UserRole
from uuid import uuid4, UUID
from sqlalchemy import Column, String

class User(SQLModel, table=True):
    id : str = Field(default_factory=lambda: str(uuid4()), nullable=False, index=True, primary_key=True)
    email: str = Field(nullable=False, unique=True, max_length=100)
    user_name: str = Field(nullable=False, unique=True, max_length=100)
    password: str = Field(nullable=False)
    role: UserRole = Field(default=UserRole.USER, nullable=False)
    my_recipes: List["Recipe"] = Relationship(back_populates="owner")