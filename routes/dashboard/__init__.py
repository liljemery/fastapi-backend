"""
Dashboard routes

Thin routes for dashboard endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from utils.auth import get_current_user
from database import get_db
from controllers.dashboard import DashboardController
from common.schemas.dashboard import DashboardResponse

dashboard_router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)


@dashboard_router.get("/", response_model=DashboardResponse)
async def get_dashboard_info(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get dashboard information for the authenticated user"""
    user_uuid = str(current_user.get("sub", ""))
    return await DashboardController.get_dashboard_info(db, user_uuid)

