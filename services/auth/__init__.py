"""
Authentication service
"""
from sqlmodel import Session, select
from typing import Optional

from database.models.user import User
from utils.auth import hash_password, verify_password
from common.exceptions.auth import UserNotFoundException, InvalidCredentialsException


class AuthService:
    """Service for authentication operations"""
    
    @staticmethod
    def create_user(db: Session, email: str, password: str, **kwargs) -> User:
        """
        Create a new user
        
        Args:
            db: Database session
            email: User email
            password: Plain text password
            **kwargs: Additional user fields
            
        Returns:
            Created user
        """
        hashed_password = hash_password(password)
        user = User(
            email=email,
            password_hash=hashed_password,
            **kwargs
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password
        
        Args:
            db: Database session
            email: User email
            password: Plain text password
            
        Returns:
            User if authentication successful, None otherwise
        """
        statement = select(User).where(
            User.email == email,
            User.deleted_at == None
        )
        user = db.exec(statement).first()
        if not user:
            return None
        
        if not verify_password(password, user.password_hash):
            return None
        
        return user
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        statement = select(User).where(
            User.email == email,
            User.deleted_at == None
        )
        return db.exec(statement).first()
    
    @staticmethod
    def get_user_by_uuid(db: Session, uuid: str) -> Optional[User]:
        """Get user by UUID"""
        statement = select(User).where(
            User.uuid == uuid,
            User.deleted_at == None
        )
        return db.exec(statement).first()

