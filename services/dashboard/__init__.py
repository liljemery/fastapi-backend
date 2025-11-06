"""
Dashboard services
"""
from sqlmodel import Session, select
from database.models.user import User
from common.exceptions.dashboard import UserNotFoundError


class DashboardServices:
    """Service for dashboard operations"""
    
    def __init__(self) -> None:
        self.users = User
    
    def get_user_by_uuid(
        self,
        user_uuid: str,
        session: Session
    ) -> User:
        """
        Get user by UUID
        
        Args:
            user_uuid: User UUID
            session: Database session
            
        Returns:
            User object
            
        Raises:
            UserNotFoundError: If user is not found
        """
        statement = select(User).where(
            User.uuid == user_uuid,
            User.deleted_at == None
        )
        query = session.exec(statement)
        user = query.first()
        
        if not user:
            raise UserNotFoundError("User not found")
        
        return user


dashboard_services = DashboardServices()

