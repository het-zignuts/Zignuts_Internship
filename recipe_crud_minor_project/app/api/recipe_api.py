from fastapi import APIRouter, HTTPException, Query, Depends
from uuid import UUID, uuid4
from typing import List, Optional
from app.schemas.recipe import RecipeCreate, RecipeUpdate, RecipeResponse, RecipePatch
from app.auth.deps import get_current_user, check_recipe_owner_or_admin
from app.models.user import User
from app.models.recipe import Recipe
from app.crud.recipe_crud import create_recipe, get_recipe, update_recipe, delete_recipe, partial_update_recipe, get_recipes
from app.db.session import db_session_manager
from sqlmodel import Session

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.post("/", response_model=RecipeResponse)
def api_create_recipe(recipe: RecipeCreate, session: Session = Depends(db_session_manager.get_session), current_user: User = Depends(get_current_user)):
    recipe_created = create_recipe(recipe, session, current_user)
    if recipe_created is None:
        raise HTTPException(status_code=400, detail="recipe could not be created")
    return recipe_created

@router.get("/{recipe_id}", response_model=RecipeResponse)
def api_get_recipe(recipe_id: UUID, session: Session = Depends(db_session_manager.get_session), current_user: User = Depends(get_current_user)):
    recipe = get_recipe(recipe_id, session)
    print("recipe OWNER:", recipe.uploaded_by)
    print("CURRENT USER:", current_user.id)
    print("ROLE:", current_user.role)
    if recipe is None:
        raise HTTPException(status_code=404, detail="recipe not found")
    if check_recipe_owner_or_admin(recipe, current_user):
        return recipe
    raise HTTPException(status_code=403, detail="Insufficient permissions")

@router.put("/{recipe_id}", response_model=RecipeResponse)
def api_update_recipe(recipe_id: UUID, new_recipe: RecipeUpdate, session: Session = Depends(db_session_manager.get_session), current_user: User = Depends(get_current_user)):
    recipe = get_recipe(recipe_id, session)
    print("recipe OWNER:", recipe.uploaded_by)
    print("CURRENT USER:", current_user.id)
    print("ROLE:", current_user.role)
    if recipe is None:
        raise HTTPException(status_code=404, detail="recipe not found")
    if check_recipe_owner_or_admin(recipe, current_user):
        updated_recipe = update_recipe(recipe_id, new_recipe, session)
        if updated_recipe is None:
            raise HTTPException(status_code=404, detail="recipe not found")
        return updated_recipe
    raise HTTPException(status_code=403, detail="Insufficient permissions")

@router.delete("/{recipe_id}", response_model=dict)
def api_delete_recipe(recipe_id: UUID, session: Session = Depends(db_session_manager.get_session), current_user: User = Depends(get_current_user)):
    print(f"Recipe id recieved in delete api as param: {recipe_id}")
    print(f"Recipe id passed to get crud: {recipe_id}")
    recipe = get_recipe(recipe_id, session)
    print("recipe OWNER:", recipe.uploaded_by)
    print("CURRENT USER:", current_user.id)
    print("ROLE:", current_user.role)
    if recipe is None:
        raise HTTPException(status_code=404, detail="recipe not found")
    print(f"Recipe recieved in api delete: {recipe.id}")
    if check_recipe_owner_or_admin(recipe, current_user):
        recipe_deleted = delete_recipe(recipe.id, session)
        if not recipe_deleted:
            raise HTTPException(status_code=404, detail="recipe not found")
        return {"detail": "recipe deleted successfully"}
    raise HTTPException(status_code=403, detail="Insufficient permissions")

@router.get("/", response_model=List[RecipeResponse])
def api_list_recipes(session: Session = Depends(db_session_manager.get_session), current_user: User = Depends(get_current_user)):
    # print("recipe OWNER:", recipe.uploaded_by)
    # print("CURRENT USER:", current_user.id)
    # print("ROLE:", current_user.role)
    recipes = get_recipes(session)
    if not recipes:
        raise HTTPException(status_code=404, detail="No recipes found")
    return recipes

@router.patch("/{recipe_id}", response_model=RecipeResponse)
def api_partial_update_recipe(recipe_id: UUID, new_recipe: RecipePatch, session: Session = Depends(db_session_manager.get_session), current_user: User = Depends(get_current_user)):
    try:
        recipe= get_recipe(recipe_id, session)
        print("recipe OWNER:", recipe.uploaded_by)
        print("CURRENT USER:", current_user.id)
        print("ROLE:", current_user.role)
        if recipe is None:
            raise HTTPException(status_code=404, detail="recipe not found")
        if check_recipe_owner_or_admin(recipe, current_user):
            updated_recipe = partial_update_recipe(recipe_id, new_recipe, session)
            if updated_recipe is None:
                raise HTTPException(status_code=404, detail="recipe not found")
            return updated_recipe
    except Exception as e:
        print("Exception occurred:", e)