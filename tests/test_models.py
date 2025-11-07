"""
Database model tests

Tests for SQLModel models and database operations
"""
import pytest
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models.user import User


@pytest.mark.asyncio
async def test_user_model_creation(async_db: AsyncSession):
    """Test user model creation"""
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash="hashed_password",
        first_name="Test",
        last_name="User"
    )
    
    async_db.add(user)
    await async_db.commit()
    await async_db.refresh(user)
    
    assert user.id is not None
    assert user.uuid is not None
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.is_active is True
    assert user.is_admin is False
    assert user.is_verified is False
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)


@pytest.mark.asyncio
async def test_user_unique_email(async_db: AsyncSession):
    """Test email uniqueness constraint"""
    user1 = User(
        email="test@example.com",
        username="user1",
        password_hash="hash1"
    )
    async_db.add(user1)
    await async_db.commit()
    
    # Try to create another user with same email
    user2 = User(
        email="test@example.com",
        username="user2",
        password_hash="hash2"
    )
    async_db.add(user2)
    
    with pytest.raises(Exception):  # Will raise IntegrityError
        await async_db.commit()


@pytest.mark.asyncio
async def test_user_uuid_generation(async_db: AsyncSession):
    """Test UUID is automatically generated"""
    user = User(
        email="test@example.com",
        password_hash="hashed_password"
    )
    
    async_db.add(user)
    await async_db.commit()
    await async_db.refresh(user)
    
    assert user.uuid is not None
    assert len(user.uuid) == 36  # UUID4 format


@pytest.mark.asyncio
async def test_user_soft_delete(async_db: AsyncSession):
    """Test soft delete functionality"""
    user = User(
        email="test@example.com",
        password_hash="hashed_password"
    )
    
    async_db.add(user)
    await async_db.commit()
    await async_db.refresh(user)
    
    # Soft delete
    user.deleted_at = datetime.utcnow()
    await async_db.commit()
    
    # Verify it's marked as deleted
    assert user.deleted_at is not None
    
    # Verify query excludes deleted users
    stmt = select(User).where(
        User.email == "test@example.com"  # type: ignore[arg-type]
    ).where(User.deleted_at.is_(None))  # type: ignore[arg-type, union-attr]
    result = await async_db.execute(stmt)
    found_user = result.scalar_one_or_none()
    
    assert found_user is None

