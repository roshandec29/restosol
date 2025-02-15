from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from typing import List
from app.config import config
Base = declarative_base()


class DBSync:
    all_sessions: List[Session] = []

    def __init__(self):
        DB_URL = config.DB_URL
        self.engine = create_engine(DB_URL)
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_new_session(self) -> Session:
        db_session = self.SessionLocal()
        self.all_sessions.append(db_session)
        return db_session

    def commit_session(self, session: Session):
        try:
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Commit failed: {e}")
            return False

    def commit_session_and_close(self, session: Session) -> bool:
        success = self.commit_session(session)
        self.close_session(session)
        return success

    def close_session(self, used_session: Session):
        try:
            if used_session in self.all_sessions:
                self.all_sessions.remove(used_session)
            used_session.close()
        except Exception as e:
            print(f"Error while closing session: {e}")
