"""Database engine and session management utilities."""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Generator, Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.infrastructure.database.models.user_model import Base

DEFAULT_SQLITE_URL = "sqlite:///./pluto.db"

DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)
ECHO_SQL = os.getenv("SQLALCHEMY_ECHO", "0") == "1"


engine = create_engine(DATABASE_URL, future=True, echo=ECHO_SQL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def init_db() -> None:
    """Create database tables based on the ORM metadata."""

    Base.metadata.create_all(bind=engine)


@contextmanager
def session_scope() -> Iterator[Session]:
    """Provide a transactional scope around a series of operations."""

    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_session() -> Generator[Session, None, None]:
    """FastAPI-compatible dependency that yields a session per request."""

    with session_scope() as session:
        yield session