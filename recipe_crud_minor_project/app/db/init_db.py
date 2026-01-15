from .session import db_session_manager
from sqlmodel import SQLModel
from app.models import user, recipe, refreshtoken

def init_db():
    SQLModel.metadata.create_all(db_session_manager.engine)