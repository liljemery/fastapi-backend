"""
Database configuration and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session
from typing import Generator, cast

from config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=settings.DEBUG
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Get database session
    
    Yields:
        Session: Database session
    """
    db = cast(Session, SessionLocal())
    try:
        yield db
    finally:
        db.close()


def get_session_sync() -> Session:
    """
    Get a synchronous database session
    
    Returns:
        Session: Database session
    """
    return cast(Session, SessionLocal())


def close_session(session: Session) -> None:
    """
    Close a database session
    
    Args:
        session: Database session to close
    """
    if session:
        session.close()


def rollback_session(session: Session) -> None:
    """
    Rollback a database session
    
    Args:
        session: Database session to rollback
    """
    if session:
        session.rollback()


def commit_session(session: Session) -> None:
    """
    Commit a database session
    
    Args:
        session: Database session to commit
    """
    if session:
        session.commit()


def init_db():
    """Initialize database tables"""
    SQLModel.metadata.create_all(bind=engine)


