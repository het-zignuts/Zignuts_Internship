from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.session import DatabaseSession
from app.crud.user import *
from app.auth.deps import get_current_user
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import AccessToken, RefreshToken
from app.core.security import Security
import datetime
import jwt

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, session: Session = Depends(DatabaseSession().get_session)):
    return create_user(session, user)

@auth_router.post("/login", response_model=UserResponse)
def login_user(user: UserCreate, session: Session = Depends(DatabaseSession().get_session)):
    user_db=get_user_by_email(session, user.email)
    if not user_db:
        raise HTTPException(status_code=400, detail="User not found, please register")
    if Security.verify_password(user.password, user_db.password):
        access_token = Security.create_access_token({"sub": user_db.id, "role": user_db.role, "iat": datetime.utcnow()})
        refresh_jwt_token = Security.create_refresh_token(user_db.id)
        Security.store_refresh_token(token_id=refresh_jwt_token["token_id"], exp_time=refresh_jwt_token["exp"], user_id=user_db.id)
        refresh_token=refresh_jwt_token["ref_token"]
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, details="Invalid password")

@auth_router.post("/refresh", response_model=AccessToken)
def refresh_access_token(refresh_token: RefreshToken, session: Session = Depends(DatabaseSession().get_session)):
    token_data = jwt.decode(refresh_token.refresh_token, Security.REFRESH_SECRET_KEY, algorithms=[Security.ALGORITHM])
    if not token_data or token_data.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token")
    ref_token_db= session.exec(select(RefreshTokenModel).where(RefreshTokenModel.token_id == token_data["token_id"])).first()
    if not ref_token_db:
        raise HTTPException(status_code=401, detail="Refresh token not found or revoked")
    new_access_token = Security.create_access_token({"sub": token_data["user_id"], "role": token_data["role"], "iat": datetime.utcnow()})
    new_refresh_jwt_token = Security.create_refresh_token(token_data["user_id"])
    Security.store_refresh_token(token_id=new_refresh_jwt_token["token_id"], exp_time=new_refresh_jwt_token["exp"], user_id=token_data["user_id"])
    session.delete(ref_token_db)
    session.commit()
    return {"access_token": new_access_token, "refresh_token": new_refresh_jwt_token["ref_token"], "token_type": "bearer"}