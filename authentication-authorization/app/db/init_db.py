from sqlmodel import SQLModel
from app.models import user, book
from app.db.session import db_session_manager

def init_db():
    SQLModel.metadata.create_all(db_session_manager.engine)