"""
Authentication request/response schemas

WHY SEPARATE FILE:
- Avoid circular imports between routes and controllers
- Reusable across routes, controllers, and services
- Clear API contract definition
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# ==================== Request Models ====================
class RegisterRequest(BaseModel):
    """User registration request"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Username")
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123!",
                "username": "johndoe",
                "first_name": "John",
                "last_name": "Doe"
            }
        }


class LoginRequest(BaseModel):
    """User login request"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123!"
            }
        }


class RefreshTokenRequest(BaseModel):
    """Refresh token request"""
    refresh_token: str = Field(..., description="Valid refresh token")


# ==================== Response Models ====================
class TokenResponse(BaseModel):
    """Token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """User response (safe fields only - never expose password_hash)"""
    uuid: str
    email: str
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    is_verified: bool
    
    class Config:
        from_attributes = True


class RegisterResponse(BaseModel):
    """Registration response"""
    user: UserResponse
    tokens: TokenResponse

