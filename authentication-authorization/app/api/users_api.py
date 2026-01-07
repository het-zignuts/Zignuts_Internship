from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db.session import DatabaseSession
from app.crud.user import *
from app.auth.deps import *
from app.schemas.user import UserCreate, UserResponse
from app.core.security import UserRole, Security
import datetime
import jwt
from app.models.user import User
from typing import List

users_router = APIRouter(prefix="/users", tags=["users"])

@users_router.get("/", response_model=List[UserResponse])
def list_users(session: Session = Depends(DatabaseSession().get_session), current_user: User = Depends(get_current_user)):
    admin = check_admin_user(current_user)
    if admin:
        users=get_all_users(session)
        return users
    else:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

@users_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, session: Session = Depends(DatabaseSession().get_session), current_user: User = Depends(get_current_user)):
    owner_or_admin = check_owner_or_admin(UUID(user_id), current_user)
    if owner_or_admin:
        user= get_user_by_id(session, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    else:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

@users_router.delete("/{user_id}", status_code=204)
def delete_user(user_id: str, session: Session = Depends(DatabaseSession().get_session), current_user: User = Depends(get_current_user)):
    owner_or_admin = check_owner_or_admin(UUID(user_id), current_user)
    if owner_or_admin:
        deleted=False
        deleted= delete_user(session, user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

@users_router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, session: Session = Depends(DatabaseSession().get_session)):
    try:
        created_user = create_user(session, user, role=UserRole.USER)
        return created_user
    except:
        raise HTTPException(status_code=400, detail="User creation failed")