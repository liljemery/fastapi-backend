"""
Authentication controller

ARCHITECTURE:
- Controllers orchestrate between routes and services
- Handle token generation, response construction
- Routes stay thin (just HTTP concerns)
- Services stay pure (just business logic)
"""
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict
import logging

from database.models.user import User
from services.auth import AuthService
from utils.auth import create_access_token, create_refresh_token
from common.schemas.auth import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    TokenResponse,
    UserResponse
)

logger = logging.getLogger(__name__)


class AuthController:
    """
    Authentication controller
    
    WHY CONTROLLER LAYER:
    - Orchestrates between routes and services
    - Handles cross-cutting concerns (token generation)
    - Routes stay thin, services stay focused on business logic
    - Easier to test each layer independently
    """
    
    @staticmethod
    def _generate_tokens(user: User) -> TokenResponse:
        """
        Generate JWT tokens for user
        
        Args:
            user: User model
            
        Returns:
            TokenResponse with access and refresh tokens
        """
        token_data = {"sub": user.uuid, "email": user.email}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
    
    @staticmethod
    def _user_to_response(user: User) -> UserResponse:
        """
        Convert User model to UserResponse
        
        Args:
            user: User model
            
        Returns:
            UserResponse (safe fields only)
        """
        return UserResponse.model_validate(user)
    
    @staticmethod
    async def register(db: AsyncSession, request: RegisterRequest) -> RegisterResponse:
        """
        Handle user registration
        
        Args:
            db: Database session
            request: Registration request data
            
        Returns:
            RegisterResponse with user data and tokens
        """
        logger.info(f"Registration attempt for email: {request.email}")
        
        # Create user (service handles validation and database)
        user = await AuthService.create_user(
            db=db,
            email=request.email,
            password=request.password,
            username=request.username,
            first_name=request.first_name,
            last_name=request.last_name
        )
        
        # Generate tokens
        tokens = AuthController._generate_tokens(user)
        
        logger.info(f"User registered successfully: {user.uuid}")
        
        return RegisterResponse(
            user=AuthController._user_to_response(user),
            tokens=tokens
        )
    
    @staticmethod
    async def login(db: AsyncSession, request: LoginRequest) -> TokenResponse:
        """
        Handle user login
        
        Args:
            db: Database session
            request: Login request data
            
        Returns:
            TokenResponse with access and refresh tokens
        """
        logger.info(f"Login attempt for email: {request.email}")
        
        # Authenticate user (service handles validation)
        user = await AuthService.authenticate_user(
            db=db,
            email=request.email,
            password=request.password
        )
        
        # Generate tokens
        tokens = AuthController._generate_tokens(user)
        
        logger.info(f"User logged in successfully: {user.uuid}")
        
        return tokens
    
    @staticmethod
    async def refresh_tokens(refresh_token: str) -> TokenResponse:
        """
        Refresh access token using refresh token
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            TokenResponse with new tokens
        """
        from utils.auth import decode_token
        from common.exceptions.auth import InvalidTokenException
        
        # Decode and validate refresh token
        payload = decode_token(refresh_token)
        
        # Verify it's a refresh token
        if payload.get("type") != "refresh":
            raise InvalidTokenException("Invalid token type")
        
        # Generate new tokens
        token_data = {"sub": payload["sub"], "email": payload.get("email")}
        access_token = create_access_token(token_data)
        new_refresh_token = create_refresh_token(token_data)
        
        logger.info(f"Tokens refreshed for user: {payload['sub']}")
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token
        )
    
    @staticmethod
    async def get_current_user_info(db: AsyncSession, user_uuid: str) -> UserResponse:
        """
        Get current user information
        
        Args:
            db: Database session
            user_uuid: User UUID from JWT token
            
        Returns:
            UserResponse with user data
        """
        user = await AuthService.get_user_by_uuid(db, user_uuid)
        assert user is not None  # get_user_by_uuid raises exception if not found
        return AuthController._user_to_response(user)
    
    @staticmethod
    def logout(user_uuid: str) -> Dict[str, str]:
        """
        Handle user logout
        
        Args:
            user_uuid: User UUID from JWT token
            
        Returns:
            Logout confirmation message
        """
        logger.info(f"User logged out: {user_uuid}")
        
        return {
            "message": "Logged out successfully",
            "detail": "Please delete your tokens on the client side"
        }

