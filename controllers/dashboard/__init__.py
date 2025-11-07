"""
Dashboard controllers

Orchestrates dashboard business logic
"""
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from services.dashboard import DashboardService
from common.schemas.dashboard import DashboardResponse
from common.exceptions.auth import UserNotFoundException

logger = logging.getLogger(__name__)


class DashboardController:
    """
    Dashboard controller
    
    """
    
    @staticmethod
    async def get_dashboard_info(db: AsyncSession, user_uuid: str) -> DashboardResponse:
        """
        Get dashboard information for user
        
        Args:
            db: Database session
            user_uuid: User UUID
            
        Returns:
            DashboardResponse with user data
            
        Raises:
            UserNotFoundException: If user not found
        """
        logger.info(f"Fetching dashboard for user: {user_uuid}")
        
        user = await DashboardService.get_user_by_uuid(db, user_uuid)
        
        return DashboardResponse(
            id=user.id or 0,
            uuid=user.uuid,
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_admin=user.is_admin,
            is_verified=user.is_verified,
            created_at=user.created_at.isoformat() if user.created_at else "",
            updated_at=user.updated_at.isoformat() if user.updated_at else ""
        )

