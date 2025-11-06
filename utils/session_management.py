from contextlib import contextmanager
from typing import Generator, Optional, Any, Callable, TypeVar, Awaitable, NoReturn, cast
from functools import wraps
from sqlmodel import Session  # type: ignore[import-untyped]
from database import SessionLocal, close_session, rollback_session, commit_session, get_session_sync
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')

@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Context manager for database sessions with automatic cleanup.
    
    Usage:
        with get_db_session() as session:
            # Use session here
            result = session.query(Model).all()
            session.commit()
    """
    session = cast(Session, SessionLocal())
    try:
        yield session
    except Exception as e:
        logger.error(f"Database session error: {e}")
        rollback_session(session)
        raise
    finally:
        close_session(session)

def safe_session_operation(operation_func: Callable[..., T]) -> Callable[..., T]:
    """Decorator to safely handle database session operations"""
    @wraps(operation_func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        session = get_session_sync()
        try:
            return operation_func(*args, session=session, **kwargs)
        except Exception as e:
            session.rollback()
            raise
        finally:
            close_session(session)
    return wrapper

class SessionManager:
    """Utility class for managing database sessions."""
    
    def __init__(self) -> None:
        self.session: Optional[Session] = None
    
    def __enter__(self) -> Session:
        self.session = cast(Session, SessionLocal())
        return self.session
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self.session:
            if exc_type is not None:
                rollback_session(self.session)
            close_session(self.session)
            self.session = None

class SessionContextManager:
    """Context manager for database sessions"""
    def __init__(self) -> None:
        self.session: Session | None = None

    def __enter__(self) -> Session:
        self.session = get_session_sync()
        return self.session

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self.session:
            close_session(self.session)

def execute_with_session(func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    """Execute a function with a database session"""
    session = get_session_sync()
    try:
        result = func(*args, session=session, **kwargs)
        return result
    except Exception as e:
        session.rollback()
        raise
    finally:
        close_session(session)

def execute_with_session_async(func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> Awaitable[T]:
    """Execute an async function with a database session"""
    session = get_session_sync()
    try:
        async def wrapper() -> T:
            return await func(*args, session=session, **kwargs)
        return wrapper()
    except Exception as e:
        session.rollback()
        raise
    finally:
        close_session(session) 