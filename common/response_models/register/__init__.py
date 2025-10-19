"""
Registration response models
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class RegisterRequest(BaseModel):
    """User registration request"""
    
    email: EmailStr
    password: str = Field(..., min_length=8)
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "newuser@example.com",
                "password": "SecurePassword123!",
                "username": "john_doe",
                "first_name": "John",
                "last_name": "Doe"
            }
        }


class RegisterResponse(BaseModel):
    """User registration response"""
    
    user_uuid: str
    email: str
    username: Optional[str] = None
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_uuid": "123e4567-e89b-12d3-a456-426614174000",
                "email": "newuser@example.com",
                "username": "john_doe",
                "message": "User registered successfully"
            }
        }

