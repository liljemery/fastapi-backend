"""
Pytest configuration and fixtures

Async test fixtures with proper database isolation
"""
import sys
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlmodel import SQLModel

from main import app
from database import get_db

# Test database (async SQLite)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create async engine for tests
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False}
)

# Create async session factory for tests
TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest_asyncio.fixture(scope="function")
async def async_db():
    """
    Async database fixture
    
    WHY ASYNC:
    - Tests should match production code (async all the way)
    - Faster tests with proper async
    """
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    # Provide session
    async with TestingSessionLocal() as session:
        yield session
    
    # Drop tables
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client(async_db):
    """
    Async test client fixture
    
    WHY ASGI TRANSPORT:
    - FastAPI routes are async
    - ASGI transport for direct async testing
    - Matches production behavior without HTTP overhead
    """
    from httpx import ASGITransport
    
    async def override_get_db():
        yield async_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


# Configure pytest-asyncio
@pytest.fixture(scope="session")
def event_loop_policy():
    """Use default event loop policy"""
    import asyncio
    return asyncio.DefaultEventLoopPolicy()


# Example async test
@pytest.mark.asyncio
async def test_health_check(client):
    """Test health check endpoint"""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

