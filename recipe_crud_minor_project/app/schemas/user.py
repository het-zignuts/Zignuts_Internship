from pydantic import BaseModel, EmailStr
from uuid import UUID
from app.core.enum import UserRole

class UserCreate(BaseModel):
    email: EmailStr
    user_name: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    role: UserRole