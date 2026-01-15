from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timedelta, timezone
from app.core.config import Config

class RefreshToken(SQLModel, table=True):
    id: str=Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)
    token_id: str=str(uuid4())
    exp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=Config.REFRESH_TOKEN_EXPIRY_TIME), nullable=False)
    user_id: str = Field(foreign_key="user.id", nullable=False)
    revoked: bool=Field(default=False)