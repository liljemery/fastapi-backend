"""
Service layer tests

Tests business logic in services without HTTP layer
"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth import AuthService
from common.exceptions.auth import (
    UserAlreadyExistsException,
    UserNotFoundException,
    InvalidCredentialsException,
    AccountInactiveException
)


@pytest.mark.asyncio
async def test_create_user(async_db: AsyncSession):
    """Test user creation"""
    user = await AuthService.create_user(
        db=async_db,
        email="test@example.com",
        password="SecurePass123!",
        username="testuser"
    )
    
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.password_hash != "SecurePass123!"  # Should be hashed
    assert user.uuid is not None
    assert user.is_active is True
    assert user.is_verified is False


@pytest.mark.asyncio
async def test_create_duplicate_user(async_db: AsyncSession):
    """Test creating user with duplicate email"""
    await AuthService.create_user(
        db=async_db,
        email="test@example.com",
        password="SecurePass123!"
    )
    
    with pytest.raises(UserAlreadyExistsException):
        await AuthService.create_user(
            db=async_db,
            email="test@example.com",
            password="AnotherPass123!"
        )


@pytest.mark.asyncio
async def test_authenticate_user_success(async_db: AsyncSession):
    """Test successful authentication"""
    # Create user
    await AuthService.create_user(
        db=async_db,
        email="test@example.com",
        password="SecurePass123!"
    )
    
    # Authenticate
    user = await AuthService.authenticate_user(
        db=async_db,
        email="test@example.com",
        password="SecurePass123!"
    )
    
    assert user.email == "test@example.com"


@pytest.mark.asyncio
async def test_authenticate_user_wrong_password(async_db: AsyncSession):
    """Test authentication with wrong password"""
    await AuthService.create_user(
        db=async_db,
        email="test@example.com",
        password="SecurePass123!"
    )
    
    with pytest.raises(InvalidCredentialsException):
        await AuthService.authenticate_user(
            db=async_db,
            email="test@example.com",
            password="WrongPassword123!"
        )


@pytest.mark.asyncio
async def test_authenticate_nonexistent_user(async_db: AsyncSession):
    """Test authentication with non-existent user"""
    with pytest.raises(InvalidCredentialsException):
        await AuthService.authenticate_user(
            db=async_db,
            email="nonexistent@example.com",
            password="SecurePass123!"
        )


@pytest.mark.asyncio
async def test_get_user_by_email(async_db: AsyncSession):
    """Test getting user by email"""
    # Create user
    created_user = await AuthService.create_user(
        db=async_db,
        email="test@example.com",
        password="SecurePass123!"
    )
    
    # Get user
    user = await AuthService.get_user_by_email(db=async_db, email="test@example.com")
    
    assert user is not None
    assert user.email == created_user.email
    assert user.uuid == created_user.uuid


@pytest.mark.asyncio
async def test_get_user_by_email_not_found(async_db: AsyncSession):
    """Test getting non-existent user by email"""
    with pytest.raises(UserNotFoundException):
        await AuthService.get_user_by_email(db=async_db, email="nonexistent@example.com")


@pytest.mark.asyncio
async def test_get_user_by_uuid(async_db: AsyncSession):
    """Test getting user by UUID"""
    # Create user
    created_user = await AuthService.create_user(
        db=async_db,
        email="test@example.com",
        password="SecurePass123!"
    )
    
    # Get user
    user = await AuthService.get_user_by_uuid(db=async_db, uuid=created_user.uuid)
    
    assert user is not None
    assert user.uuid == created_user.uuid


@pytest.mark.asyncio
async def test_authenticate_inactive_account(async_db: AsyncSession):
    """Test authentication with inactive account"""
    # Create user
    user = await AuthService.create_user(
        db=async_db,
        email="test@example.com",
        password="SecurePass123!"
    )
    
    # Deactivate account
    user.is_active = False
    async_db.add(user)
    await async_db.commit()
    
    # Try to authenticate
    with pytest.raises(AccountInactiveException):
        await AuthService.authenticate_user(
            db=async_db,
            email="test@example.com",
            password="SecurePass123!"
        )

