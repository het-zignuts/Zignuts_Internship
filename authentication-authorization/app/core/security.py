from passlib.context import CryptContext
from app.core.config import Config
from datetime import datetime, timedelta
from jose import JWTError, jwt
from enum import Enum
from uuid import uuid4
from app.models.refreshtoken import RefreshToken
from app.db.session import DatabaseSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user

class Security:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict) -> str:
        payload = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=Config.TOKEN_EXPIRY_TIME)
        payload.update({"exp": expire})
        payload.update({"type": "access"})
        encoded_jwt = jwt.encode(payload, Config.SECRET_KEY, Config.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_access_token(token: str) -> dict | None:
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
            return payload
        except JWTError:
            return None

    @staticmethod
    def create_refresh_token(user_id: UUID):
        created_at=datetime.utcnow()
        exp_time=datetime.utcnow() + timedelta(days=Config.REFRESH_EXPIRY_TIME)
        token_id=str(uuid4())
        payload={
            "sub": user_id,
            "token_id": token_id,
            "created_at": created_at,
            "exp": exp_time,
            "type": "refresh"
        }
        encoded_refresh_jwt=jwt.encode(payload, Config.REFRESH_SECRET_KEY, Config.ALGORITHM)
        return {
            "ref_token": encoded_refresh_jwt,
            "token_id": token_id,
            "created_at": created_at,
            "exp": exp_time
            }

    @staticmethod
    def store_refresh_token(session: Session=Depends(DatabaseSession().get_session), token_id: str, exp_time: datetime, user_id: UUID):
        token=RefreshToken(token_id=token_id, exp=exp_time, user_id=user_id)
        session.add(token)
        session.commit()
        session.refresh(token)



# from datetime import datetime, timedelta
# from enum import Enum
# from typing import Any, Optional

# from jose import jwt
# from passlib.context import CryptContext

# from app.core.config import settings


# # -------------------------------
# # Password hashing
# # -------------------------------

# pwd_context = CryptContext(
#     schemes=["bcrypt"],
#     deprecated="auto"
# )


# def hash_password(password: str) -> str:
#     """
#     Hash a plain-text password.
#     """
#     return pwd_context.hash(password)


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """
#     Verify a password against its hash.
#     """
#     return pwd_context.verify(plain_password, hashed_password)


# # -------------------------------
# # User Roles
# # -------------------------------

# class UserRole(str, Enum):
#     USER = "user"
#     ADMIN = "admin"


# # -------------------------------
# # JWT helpers
# # -------------------------------

# def _create_token(
#     subject: str | int,
#     token_type: str,
#     expires_delta: timedelta,
#     extra_claims: Optional[dict[str, Any]] = None,
# ) -> str:
#     """
#     Internal helper for creating JWT tokens.
#     """
#     payload = {
#         "sub": str(subject),
#         "type": token_type,
#         "iat": datetime.utcnow(),
#         "exp": datetime.utcnow() + expires_delta,
#     }

#     if extra_claims:
#         payload.update(extra_claims)

#     return jwt.encode(
#         payload,
#         settings.SECRET_KEY,
#         algorithm=settings.ALGORITHM,
#     )


# def create_access_token(
#     user_id: int,
#     role: UserRole,
# ) -> str:
#     """
#     Short-lived access token.
#     """
#     return _create_token(
#         subject=user_id,
#         token_type="access",
#         expires_delta=timedelta(
#             minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
#         ),
#         extra_claims={"role": role.value},
#     )


# def create_refresh_token(user_id: int) -> str:
#     """
#     Long-lived refresh token.
#     """
#     return _create_token(
#         subject=user_id,
#         token_type="refresh",
#         expires_delta=timedelta(
#             days=settings.REFRESH_TOKEN_EXPIRE_DAYS
#         ),
#     )
