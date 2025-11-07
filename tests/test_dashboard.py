"""
Dashboard endpoint tests

Tests for dashboard routes and controllers
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_get_dashboard_authenticated(client: AsyncClient, async_db: AsyncSession):
    """Test getting dashboard with valid token"""
    # Register user and get token
    register_response = await client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "SecurePass123!",
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User"
        }
    )
    
    access_token = register_response.json()["tokens"]["access_token"]
    
    # Get dashboard
    response = await client.get(
        "/api/dashboard/",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert data["first_name"] == "Test"
    assert data["last_name"] == "User"
    assert data["is_active"] is True
    assert "uuid" in data


@pytest.mark.asyncio
async def test_get_dashboard_no_token(client: AsyncClient):
    """Test getting dashboard without authentication"""
    response = await client.get("/api/dashboard/")
    
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_dashboard_invalid_token(client: AsyncClient):
    """Test getting dashboard with invalid token"""
    response = await client.get(
        "/api/dashboard/",
        headers={"Authorization": "Bearer invalid_token"}
    )
    
    assert response.status_code == 401

