"""
Routes package
"""

from routes.auth import router as auth_router
from routes.dashboard import dashboard_router

from fastapi import APIRouter  # type: ignore[import-untyped]
router = APIRouter()
router.include_router(auth_router)
router.include_router(dashboard_router)

__all__ = ["router"]