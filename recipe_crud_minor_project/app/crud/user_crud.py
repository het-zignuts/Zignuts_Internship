from app.models.user import User
from app.models.recipe import Recipe
from sqlmodel import Session, select
# from fastapi import HTTPException
from typing import Optional
from app.schemas.user import UserCreate, UserResponse
# from app.db.session import DatabaseSession
from app.core.security import Security
from app.core.enum import UserRole
# from fastapi import Depends
# from app.models.user import User

def create_user(session: Session, user: UserCreate, role: UserRole = UserRole.USER) -> UserResponse | None:
    if (session.exec(select(User).where(User.email == user.email)).first()):
        return None
    hashed_password = Security.hash_password(user.password)
    user_instance=User(email=user.email, user_name=user.user_name,password=hashed_password, role=role)
    session.add(user_instance)
    session.commit()
    session.refresh(user_instance)
    return UserResponse(id=user_instance.id, email=user_instance.email, role=user_instance.role)

def get_user_by_email(session: Session, email: str) -> Optional[UserResponse]:
    user_instance = session.exec(select(User).where(User.email == email)).first()
    if user_instance:
        return UserResponse(id=user_instance.id, email=user_instance.email, role=user_instance.role)
    return None

def get_user_by_id(session: Session, user_id: UUID) -> Optional[UserResponse]:
    user_instance = session.exec(select(User).where(User.id == user_id)).first()
    if user_instance:
        return UserResponse(id=user_instance.id, email=user_instance.email, role=user_instance.role)
    return None

def get_user_model_instance(session: Session, user_id: UUID) -> Optional[User]:
    user_instance = session.exec(select(User).where(User.id == user_id)).first()
    if user_instance:
        return user_instance
    return None

def get_all_users(session: Session) -> list[UserResponse]:
    users = session.exec(select(User)).all()
    return [UserResponse(id=user.id, email=user.email, role=user.role) for user in users]

def delete_user_by_id(user_id: UUID, session: Session) -> bool:
    user_instance = session.exec(select(User).where(User.id == user_id)).first()
    if not user_instance:
        raise HTTPException(status_code=404, detail="User not found")
    user_recipes=session.exec(select(Recipe).where(Recipe.uploaded_by == user_id)).all()
    for recipe in user_recipes:
        session.delete(recipe)
    session.delete(user_instance)
    session.commit()
    return True