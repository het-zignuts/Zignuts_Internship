from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=20)

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    role: str