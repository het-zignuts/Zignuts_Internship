from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional, Dict 
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from sqlalchemy import Column, JSON
from app.core.enum import RecipeCategory
from sqlalchemy.orm import Mapped
from sqlalchemy import Column, String, ForeignKey

class Recipe(SQLModel, table=True):
    id : str = Field(default_factory=lambda: str(uuid4()), nullable=False, index=True, primary_key=True)
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
    uploaded_by: str = Field(foreign_key="user.id", nullable=False)
    owner: Mapped[Optional["User"]] = Relationship(back_populates="my_recipes")