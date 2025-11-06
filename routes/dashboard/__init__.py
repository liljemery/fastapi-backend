"""
Dashboard routes
"""
from fastapi import APIRouter, Request  # type: ignore[import-untyped]
from fastapi.responses import JSONResponse  # type: ignore[import-untyped] 
from controllers.dashboard import get_dashboard_info_controller
from common.response_models.error_response import generate_error_response_for_statuses
from typing import cast, Dict, Any, Union

dashboard_router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)


@dashboard_router.get(
    "/",
    name="Get Dashboard Info",
    summary="Get Dashboard Information",
    description="Retrieves dashboard information for the authenticated user",
    responses=cast(Dict[Union[int, str], Dict[str, Any]], generate_error_response_for_statuses([400, 404, 422, 500]))
)
async def get_dashboard_info(request: Request) -> JSONResponse:
    """
    Get dashboard information endpoint
    
    Args:
        request: FastAPI request object
        
    Returns:
        JSONResponse with dashboard data
    """
    return await get_dashboard_info_controller(request)

