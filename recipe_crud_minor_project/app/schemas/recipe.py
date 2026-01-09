from pydantic import BaseModel, Field
from typing import List, Optional
from app.core.enum import RecipeCategory
from datetime import datetime
from uuid import UUID

class RecipeCreate(BaseModel):
    title : str 
    description : str | None
    ingredients: List[str] 
    instructions : str 
    time_taken: int 
    serving: str
    cuisine: str | None 
    category: RecipeCategory 
    image_url: str | None 

class RecipeUpdate(BaseModel):
    title : str 
    description : str | None
    ingredients: List[str] 
    instructions : str 
    time_taken: int 
    serving: str
    cuisine: str | None 
    category: RecipeCategory 
    image_url: str | None 

class RecipePatch(BaseModel):
    title : str | None = None
    description : str | None = None
    ingredients: List[str] | None = None
    instructions : str | None = None
    time_taken: int | None = None
    serving: str | None = None
    cuisine: str | None = None
    category: RecipeCategory | None = None
    image_url: str | None = None

class RecipeResponse(BaseModel):
    id: UUID
    title: str
    cuisine: str
    category: RecipeCategory
    created_at: datetime
    updated_at: datetime
    uploaded_by: UUID
