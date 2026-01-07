from sqlmodel import create_engine, Session
from app.core.config import Config

class DatabaseSession:
    def __init__(self):
        self.engine = create_engine(Config.DATABASE_URL, echo=True)

    def get_session(self) -> Session:
        with Session(self.engine) as session:
            yield session