"""
Database configuration and session management

Production-grade async database setup with proper connection pooling
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlmodel import SQLModel, Session
from typing import AsyncGenerator, Generator, Dict, Any
from contextlib import asynccontextmanager, contextmanager
import logging

from config import settings

logger = logging.getLogger(__name__)


def _get_sync_database_url(url: str) -> str:
    """
    Convert database URL to sync version with explicit driver

    """
    if "postgresql://" in url and "postgresql+" not in url:
        return url.replace("postgresql://", "postgresql+psycopg2://")
    return url


def _get_async_database_url(url: str) -> str:
    """
    Convert database URL to async version
    
    WHY:
    - Auto-detects database type
    - Uses psycopg for async PostgreSQL operations
    """
    if "sqlite" in url and "aiosqlite" not in url:
        return url.replace("sqlite://", "sqlite+aiosqlite://")
    elif "postgresql://" in url:
        # Use psycopg (v3) for async PostgreSQL
        return url.replace("postgresql://", "postgresql+psycopg://")
    return url


# Sync engine for migrations and CLI tools
engine_kwargs: Dict[str, Any] = {"echo": settings.DEBUG}

if "sqlite" in settings.DATABASE_URL:
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    engine_kwargs.update({
        "pool_pre_ping": True,
        "pool_size": 5,
        "max_overflow": 10,
    })

engine = create_engine(_get_sync_database_url(settings.DATABASE_URL), **engine_kwargs)

# Async engine for API endpoints
async_engine_kwargs: Dict[str, Any] = {"echo": settings.DEBUG}

if "sqlite" not in settings.DATABASE_URL:
    async_engine_kwargs.update({
        "pool_pre_ping": True,
        "pool_size": 5,
        "max_overflow": 10,
    })

async_engine = create_async_engine(
    _get_async_database_url(settings.DATABASE_URL),
    **async_engine_kwargs
)

# Session factories
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for async database sessions
    
    USAGE:
        @app.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(User))
            return result.scalars().all()
    
    WHY ASYNC:
    - Non-blocking I/O for better concurrency
    - FastAPI is async-native
    - Production APIs should never block on database calls
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database error: {e}", exc_info=True)
            raise
        finally:
            await session.close()


@asynccontextmanager
async def async_session_scope() -> AsyncGenerator[AsyncSession, None]:
    """
    Async context manager for database operations outside FastAPI requests
    
    USAGE:
        async with async_session_scope() as session:
            user = await session.get(User, user_id)
            user.name = "Updated"
            await session.commit()
    
    WHY:
    - Single pattern for background tasks, workers, scripts
    - Automatic rollback on exceptions
    - Proper cleanup guaranteed
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Session error: {e}", exc_info=True)
            raise
        finally:
            await session.close()


@contextmanager
def sync_session_scope() -> Generator[Session, None, None]:
    """
    Sync context manager for migrations and CLI tools
    
    USAGE:
        with sync_session_scope() as session:
            user = session.get(User, user_id)
            user.name = "Updated"
    
    WHY KEEP SYNC:
    - Alembic migrations are synchronous
    - CLI scripts may not need async overhead
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Session error: {e}", exc_info=True)
        raise
    finally:
        session.close()


def init_db() -> None:
    """
    Initialize database tables
    
    WHY SYNC:
    - Called once at startup before async event loop
    - SQLModel.metadata operations are synchronous
    """
    try:
        SQLModel.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}", exc_info=True)
        raise


async def close_db() -> None:
    """
    Cleanup database connections on shutdown
    
    WHY:
    - Graceful shutdown prevents connection leaks
    - Important for containerized deployments
    """
    await async_engine.dispose()
    engine.dispose()
    logger.info("Database connections closed")
