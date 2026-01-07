from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import Config
from app.core.security import Security
from uuid import UUID
from app.models.user import User
from app.models.book import Book
from app.core.security import UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(session : Session = Depends(DatabaseSession().get_session), token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, Config.SECRET_KEY,algorithms=[settings.ALGORITHM])
        if payload:
            user_id: str = payload.get("sub")
            tkn_type: str|None=payload.get("type")
            if user_id is None or tkn_type is None:
                raise HTTPException(status_code=401, details="Invalid authentication credentials")
            user= session.get(User, UUID(user_id))
            if not user:
                raise HTTPExcetion(status_code=401, details="User not found...")
            return user
        else:
            raise HTTPException(status_code=401, details="Authentication failed...")
    except JWTError:
        raise HTTPException(status_code=401, details="Invalid authentication credentials")

def check_admin_user(current_user: User = Depends(get_current_user)) -> bool:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return True

def check_owner_or_admin(user_id: UUID, current_user: User = Depends(get_current_user)) -> bool:
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return True

def check_book_owner_or_admin(book: Book, user:User)->bool:
    if user.role != UserRole.ADMIN or book.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return True