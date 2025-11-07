"""
Utility function tests

Tests for authentication utilities, password hashing, etc.
"""
import pytest
from jose import jwt

from utils.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)
from config import settings
from common.exceptions.auth import InvalidTokenException


def test_hash_password():
    """Test password hashing"""
    password = "SecurePass123!"
    hashed = hash_password(password)
    
    assert hashed != password
    assert len(hashed) > 0
    assert hashed.startswith("$2b$")  # bcrypt prefix


def test_verify_password():
    """Test password verification"""
    password = "SecurePass123!"
    hashed = hash_password(password)
    
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_create_access_token():
    """Test access token creation"""
    data = {"sub": "user-uuid-123", "email": "test@example.com"}
    token = create_access_token(data)
    
    assert isinstance(token, str)
    assert len(token) > 0
    
    # Decode and verify
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["sub"] == "user-uuid-123"
    assert payload["email"] == "test@example.com"
    assert payload["type"] == "access"


def test_create_refresh_token():
    """Test refresh token creation"""
    data = {"sub": "user-uuid-123", "email": "test@example.com"}
    token = create_refresh_token(data)
    
    assert isinstance(token, str)
    assert len(token) > 0
    
    # Decode and verify
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["sub"] == "user-uuid-123"
    assert payload["type"] == "refresh"


def test_decode_token():
    """Test token decoding"""
    data = {"sub": "user-uuid-123", "email": "test@example.com"}
    token = create_access_token(data)
    
    payload = decode_token(token)
    
    assert payload["sub"] == "user-uuid-123"
    assert payload["email"] == "test@example.com"
    assert payload["type"] == "access"


def test_decode_invalid_token():
    """Test decoding invalid token"""
    from fastapi import HTTPException
    
    with pytest.raises(HTTPException) as exc_info:
        decode_token("invalid_token_string")
    
    assert exc_info.value.status_code == 401

