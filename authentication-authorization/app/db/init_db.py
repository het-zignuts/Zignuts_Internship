from sqlmodel import SQLModel
from app.models import user, book
from .session import DatabaseSession

def init_db():
    db_session = DatabaseSession()
    engine = db_session.engine
    SQLModel.metadata.create_all(engine)