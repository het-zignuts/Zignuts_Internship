from app.models.user import User
from sqlmodel import Session, select
from fastapi import HTTPException
from typing import Optional
from app.schemas.user import UserCreate, UserResponse
from app.db.session import DatabaseSession
from app.core.security import UserRole, Security

def create_user(session: Session, user: UserCreate, role: UserRole = UserRole.USER) -> UserResponse:
    if (session.exec(select(User).where(User.email == user.email)).first()):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = Security.hash_password(user.password)
    user_instance=User(email=user.email, password=hashed_password, role=role)
    session.add(user_instance)
    session.commit()
    session.refresh(user_instance)
    return UserResponse(id=user_instance.id, email=user_instance.email, role=user_instance.role)

def get_user_by_email(session: Session, email: str) -> Optional[UserResponse]:
    user_instance = session.exec(select(User).where(User.email == email)).first()
    if user_instance:
        return UserResponse(id=user_instance.id, email=user_instance.email, role=user_instance.role)
    return None

def get_user_by_id(session: Session, user_id: str) -> Optional[UserResponse]:
    user_instance = session.exec(select(User).where(User.id == user_id)).first()
    if user_instance:
        return UserResponse(id=user_instance.id, email=user_instance.email, role=user_instance.role)
    return None

def get_all_users(session: Session) -> list[UserResponse]:
    users = session.exec(select(User)).all()
    return [UserResponse(id=user.id, email=user.email, role=user.role) for user in users]

def delete_user(session: Session, user_id: str) -> bool:
    user_instance = session.exec(select(User).where(User.id == user_id)).first()
    if not user_instance:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user_instance)
    session.commit()
    return True