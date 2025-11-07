"""
Authentication tests

Tests for registration, login, token refresh, and user endpoints
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.user import User
from services.auth import AuthService


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient, async_db: AsyncSession):
    """Test successful user registration"""
    response = await client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "SecurePass123!",
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["user"]["email"] == "test@example.com"
    assert data["user"]["username"] == "testuser"
    assert "access_token" in data["tokens"]
    assert "refresh_token" in data["tokens"]


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, async_db: AsyncSession):
    """Test registration with existing email"""
    # Create first user
    await client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "SecurePass123!"}
    )
    
    # Try to register again with same email
    response = await client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "AnotherPass123!"}
    )
    
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_register_weak_password(client: AsyncClient):
    """Test registration with weak password"""
    response = await client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "weak"}
    )
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, async_db: AsyncSession):
    """Test successful login"""
    # Register user first
    await client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "SecurePass123!"}
    )
    
    # Login
    response = await client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "SecurePass123!"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient, async_db: AsyncSession):
    """Test login with invalid credentials"""
    # Register user
    await client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "SecurePass123!"}
    )
    
    # Try wrong password
    response = await client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "WrongPassword123!"}
    )
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    """Test login with non-existent user"""
    response = await client.post(
        "/api/auth/login",
        json={"email": "nonexistent@example.com", "password": "SecurePass123!"}
    )
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, async_db: AsyncSession):
    """Test getting current user information"""
    # Register and get tokens
    register_response = await client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "SecurePass123!"}
    )
    
    access_token = register_response.json()["tokens"]["access_token"]
    
    # Get current user
    response = await client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_get_current_user_no_token(client: AsyncClient):
    """Test getting current user without token"""
    response = await client.get("/api/auth/me")
    
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient, async_db: AsyncSession):
    """Test token refresh"""
    # Register and get tokens
    register_response = await client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "SecurePass123!"}
    )
    
    refresh_token = register_response.json()["tokens"]["refresh_token"]
    
    # Refresh token
    response = await client.post(
        "/api/auth/refresh-token",
        json={"refresh_token": refresh_token}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_refresh_token_invalid(client: AsyncClient):
    """Test token refresh with invalid token"""
    response = await client.post(
        "/api/auth/refresh-token",
        json={"refresh_token": "invalid_token"}
    )
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_logout(client: AsyncClient, async_db: AsyncSession):
    """Test logout endpoint"""
    # Register and get tokens
    register_response = await client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "SecurePass123!"}
    )
    
    access_token = register_response.json()["tokens"]["access_token"]
    
    # Logout
    response = await client.post(
        "/api/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert response.status_code == 200

