from typing import List, Optional
from sqlmodel import Session, select
from app.schemas.recipe import RecipeCreate, RecipeResponse, RecipeUpdate, RecipePatch
from app.models.recipe import Recipe
from app.models.user import User

def create_recipe(recipe: RecipeCreate, session: Session, current_user: User) -> RecipeResponse:
    recipe=Recipe(**recipe.model_dump())
    recipe.uploaded_by = current_user.id
    session.add(recipe)
    session.commit()
    session.refresh(recipe)
    return RecipeResponse(**recipe.model_dump())
    
def get_recipe(recipe_id: UUID, session: Session) -> Optional[RecipeResponse]:
    recipe=session.get(Recipe, recipe_id)
    if recipe:
        return RecipeResponse(**recipe.model_dump())
    return None

def get_recipes(session: Session) -> List[RecipeResponse]:
    query = select(Recipe)
    # if author:
    #     query = query.where(Book.author == author)
    recipes = session.exec(query).all()
    return [RecipeResponse(**recipe.model_dump()) for recipe in recipes]

def partial_update_recipe(recipe_id: UUID, new_data: RecipePatch, session: Session) -> Optional[RecipeResponse]:
    recipe=session.get(Recipe, recipe_id)
    if not recipe:
        return None
    recipe_data=new_data.model_dump(exclude_unset=True)
    for key, value in recipe_data.items():
        setattr(recipe, key, value)
    session.add(recipe)
    session.commit()
    session.refresh(recipe)
    return RecipeResponse(**recipe.model_dump())

def update_recipe(recipe_id: UUID, new_data: RecipeUpdate, session: Session) -> Optional[RecipeResponse]:
    recipe=session.get(Recipe, recipe_id)
    if not recipe:
        return None
    recipe_data=new_data.model_dump()
    for key, value in recipe_data.items():
        setattr(recipe, key, value)
    session.add(recipe)
    session.commit()
    session.refresh(recipe)
    return RecipeResponse(**recipe.model_dump())

def delete_recipe(recipe_id: UUID, session: Session) -> bool:
    recipe=session.get(Recipe, recipe_id)
    if not recipe:
        return False
    session.delete(recipe)
    session.commit()
    return True