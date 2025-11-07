"""
Authentication routes

THIN ROUTES - Only HTTP concerns (validation, dependency injection)
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from utils.auth import get_current_user
from controllers.auth import AuthController
from common.schemas.auth import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    RefreshTokenRequest,
    TokenResponse,
    UserResponse
)

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


# ==================== Endpoints ====================
@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user account
    
    Creates user and returns JWT tokens for immediate login.
    """
    return await AuthController.register(db, request)


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    User login
    
    Authenticates user and returns JWT tokens.
    """
    return await AuthController.login(db, request)


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """
    User logout
    
    With JWT, logout is client-side (delete tokens).
    This endpoint logs the event for audit trail.
    """
    user_uuid = str(current_user.get("sub", ""))
    return AuthController.logout(user_uuid)


@router.post("/refresh-token", response_model=TokenResponse)
async def refresh_token(request: RefreshTokenRequest):
    """
    Refresh access token
    
    Accepts refresh token and returns new tokens.
    """
    return await AuthController.refresh_tokens(request.refresh_token)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current user information
    
    Requires valid access token in Authorization header.
    """
    user_uuid = str(current_user.get("sub", ""))
    return await AuthController.get_current_user_info(db, user_uuid)

