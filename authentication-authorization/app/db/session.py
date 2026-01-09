from sqlmodel import create_engine, Session
from app.core.config import Config

engine=create_engine(Config.DATABASE_URL, echo=True)

class DatabaseSession:
    def __init__(self, engine):
        self.engine = engine

    def get_session(self) -> Session:
        with Session(self.engine) as session:
            yield session


db_session_manager=DatabaseSession(engine)
print("DB INSTANCE ID:", id(db_session_manager))
