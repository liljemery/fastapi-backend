"""
Authentication routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from common.response_models.login import *
from common.response_models.register import *

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(db: Session = Depends(get_db)):
    """Register a new user"""
    return {"message": "Register endpoint - to be implemented"}


@router.post("/login")
async def login(db: Session = Depends(get_db)):
    """User login"""
    return {"message": "Login endpoint - to be implemented"}


@router.post("/logout")
async def logout():
    """User logout"""
    return {"message": "Logout endpoint - to be implemented"}


@router.post("/refresh-token")
async def refresh_token():
    """Refresh access token"""
    return {"message": "Refresh token endpoint - to be implemented"}

