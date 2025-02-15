from contextlib import contextmanager
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from typing import List, Generator
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


class DBManager:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self._sessionmaker = None

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        db = self.SessionLocal()
        try:
            yield db
            db.commit()
        except Exception as e:
            db.rollback()
            raise
        finally:
            db.close()


@lru_cache
def init_db(db_url: str = config.DB_URL):
    return DBManager(db_url)


def get_db() -> Session:
    db_manager = init_db()
    with db_manager.session() as db:
        yield db
