"""
Authentication service
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, cast
import logging

from database.models.user import User
from utils.auth import hash_password, verify_password
from common.exceptions.auth import (
    UserNotFoundException,
    InvalidCredentialsException,
    UserAlreadyExistsException,
    AccountInactiveException,
    EmailNotVerifiedException
)

logger = logging.getLogger(__name__)


class AuthService:
    """
    Service for authentication operations
    
    """
    
    @staticmethod
    async def create_user(
        db: AsyncSession,
        email: str,
        password: str,
        username: Optional[str] = None,
        **kwargs
    ) -> User:
        """
        Create a new user account
        
        Args:
            db: Async database session
            email: User email (must be unique)
            password: Plain text password (will be hashed)
            username: Optional username
            **kwargs: Additional user fields (first_name, last_name, etc.)
            
        Returns:
            Created user object
            
        Raises:
            UserAlreadyExistsException: If email/username already exists
        """
        existing_email = await AuthService.get_user_by_email(db, email, raise_if_not_found=False)
        if existing_email:
            logger.warning(f"Attempted to create user with existing email: {email}")
            raise UserAlreadyExistsException(field="email")
        
        if username:
            stmt = select(User).where(User.username == username).where(User.deleted_at.is_(None))  # type: ignore[arg-type, union-attr]
            result = await db.execute(stmt)
            existing_username = result.scalar_one_or_none()
            if existing_username:
                logger.warning(f"Attempted to create user with existing username: {username}")
                raise UserAlreadyExistsException(field="username")
        
        # Hash password and create user
        hashed_password = hash_password(password)
        user = User(
            email=email,
            username=username,
            password_hash=hashed_password,
            **kwargs
        )
        
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        logger.info(f"Created new user: {user.uuid} ({email})")
        return user
    
    @staticmethod
    async def authenticate_user(db: AsyncSession, email: str, password: str) -> User:
        """
        Authenticate user with email and password
        
        Args:
            db: Async database session
            email: User email
            password: Plain text password
            
        Returns:
            Authenticated user object
            
        Raises:
            InvalidCredentialsException: If credentials are invalid
            AccountInactiveException: If account is inactive
            EmailNotVerifiedException: If email not verified (optional check)
        """
        try:
            user = await AuthService.get_user_by_email(db, email, raise_if_not_found=True)
        except UserNotFoundException:
            logger.warning(f"Failed login attempt for email: {email} - Invalid credentials")
            raise InvalidCredentialsException()
        
        assert user is not None, "User should not be None when raise_if_not_found=True"
        
        if not verify_password(password, user.password_hash):
            logger.warning(f"Failed login attempt for user: {user.uuid} - Invalid credentials")
            raise InvalidCredentialsException()
        
        if not user.is_active:
            logger.warning(f"Login attempt for inactive account: {user.uuid} - Account inactive")
            raise AccountInactiveException()
        
        # Optional: Check if email is verified
        # Uncomment if you want to enforce email verification
        # if not user.is_verified:
        #     logger.warning(f"Login attempt for unverified account: {user.uuid}")
        #     raise EmailNotVerifiedException()
        
        logger.info(f"Successful authentication for user: {user.uuid}")
        return user
    
    @staticmethod
    async def get_user_by_email(
        db: AsyncSession,
        email: str,
        raise_if_not_found: bool = True
    ) -> Optional[User]:
        """
        Get user by email
        
        Args:
            db: Async database session
            email: User email
            raise_if_not_found: If True, raise exception when not found
            
        Returns:
            User object or None
            
        Raises:
            UserNotFoundException: If user not found and raise_if_not_found=True
        """
        stmt = select(User).where(User.email == email).where(User.deleted_at.is_(None))  # type: ignore[arg-type, union-attr]
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user and raise_if_not_found:
            raise UserNotFoundException(identifier=email)
        
        return user
    
    @staticmethod
    async def get_user_by_uuid(
        db: AsyncSession,
        uuid: str,
        raise_if_not_found: bool = True
    ) -> Optional[User]:
        """
        Get user by UUID
        
        Args:
            db: Async database session
            uuid: User UUID
            raise_if_not_found: If True, raise exception when not found
            
        Returns:
            User object or None
            
        Raises:
            UserNotFoundException: If user not found and raise_if_not_found=True
        """
        stmt = select(User).where(User.uuid == uuid).where(User.deleted_at.is_(None))  # type: ignore[arg-type, union-attr]
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user and raise_if_not_found:
            raise UserNotFoundException(identifier=uuid)
        
        return user
    
    @staticmethod
    async def get_user_by_id(
        db: AsyncSession,
        user_id: int,
        raise_if_not_found: bool = True
    ) -> Optional[User]:
        """
        Get user by ID
        
        Args:
            db: Async database session
            user_id: User ID
            raise_if_not_found: If True, raise exception when not found
            
        Returns:
            User object or None
            
        Raises:
            UserNotFoundException: If user not found and raise_if_not_found=True
        """
        stmt = select(User).where(User.id == user_id).where(User.deleted_at.is_(None))  # type: ignore[arg-type, union-attr]
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user and raise_if_not_found:
            raise UserNotFoundException(identifier=str(user_id))
        
        return user

