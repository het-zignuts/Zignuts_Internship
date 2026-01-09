from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional, Dict 
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from sqlalchemy import Column, JSON
from app.core.enum import RecipeCategory
from sqlalchemy.orm import Mapped

class Recipe(SQLModel, table=True):
    id : UUID = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)
    title : str = Field(max_length=50, nullable=False) 
    # email : str = Field(max_length=100, nullable=False, unique=True)
    description : str | None = Field(max_length=500, nullable=True,default=None)  
    ingredients: List[str] = Field(sa_column=Column(JSON, nullable=False))  
    instructions : str = Field(nullable=False) 
    time_taken: int = Field(nullable=False, ge=0) 
    serving: str = Field(nullable=False) 
    cuisine: str | None = Field(nullable=True, default=None) 
    category: RecipeCategory = Field(nullable=False, default=RecipeCategory.SNACK)  
    image_url: str | None = Field(nullable=True, default=None)  
    created_at: datetime = Field(nullable=False, default_factory=lambda: datetime.utcnow())
    updated_at: datetime = Field(nullable=False, default_factory=lambda: datetime.utcnow())
    uploaded_by: UUID = Field(nullable=False, foreign_key="user.id")
    owner: Mapped[Optional["User"]] = Relationship(back_populates="my_recipes")