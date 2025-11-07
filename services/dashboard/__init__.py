"""
Dashboard service

Business logic for dashboard operations
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

from database.models.user import User
from common.exceptions.auth import UserNotFoundException

logger = logging.getLogger(__name__)


class DashboardService:
    """
    Dashboard service
    
    Handles dashboard-related business logic
    """
    
    @staticmethod
    async def get_user_by_uuid(db: AsyncSession, user_uuid: str) -> User:
        """
        Get user by UUID for dashboard
        
        Args:
            db: Database session
            user_uuid: User UUID
            
        Returns:
            User object
            
        Raises:
            UserNotFoundException: If user not found
        """
        stmt = select(User).where(User.uuid == user_uuid).where(User.deleted_at.is_(None))  # type: ignore[arg-type, union-attr]
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            raise UserNotFoundException(identifier=user_uuid)
        
        return user
