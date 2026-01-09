from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db.session import db_session_manager
from app.crud.user_crud import *
from app.auth.deps import *
from app.schemas.user import UserCreate, UserResponse
from app.core.security import Security
from app.core.enum import UserRole
from app.models.user import User
from typing import List
from uuid import UUID

users_router = APIRouter(prefix="/users", tags=["users"])

@users_router.get("/", response_model=List[UserResponse])
def list_users(session: Session = Depends(db_session_manager.get_session), current_user: User = Depends(get_current_user)):
    admin = check_admin_user(current_user)
    if admin:
        users=get_all_users(session)
        return users
    else:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

@users_router.get("/me", response_model=UserResponse)
def get_user_me(current_user: User = Depends(get_current_user)):
    if check_owner_or_admin(current_user.id, current_user):
        return current_user
    raise HTTPException(status_code=403, detail="Insufficient permissions")

@users_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: UUID, session: Session = Depends(db_session_manager.get_session), current_user: User = Depends(get_current_user)):
    owner_or_admin = check_owner_or_admin(user_id, current_user)
    print(owner_or_admin)
    if owner_or_admin:
        user= get_user_by_id(session, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    else:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

@users_router.delete("/me", status_code=204)
def delete_user_me(current_user: User = Depends(get_current_user), session: Session = Depends(db_session_manager.get_session)):
    if check_owner_or_admin(current_user.id, current_user):
        deleted = delete_user_by_id(current_user.id, session)
        return
        if not deleted:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

@users_router.delete("/{user_id}", status_code=204)
def delete_user_api(user_id: UUID, session: Session = Depends(db_session_manager.get_session), current_user: User = Depends(get_current_user)):
    owner_or_admin = check_owner_or_admin(user_id, current_user)
    if owner_or_admin:
        deleted=False
        deleted= delete_user_by_id(user_id, session)
        if not deleted:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

@users_router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, session: Session = Depends(db_session_manager.get_session)):
    try:
        created_user = create_user(session, user, role=UserRole.USER)
        return created_user
    except:
        raise HTTPException(status_code=400, detail="User creation failed")