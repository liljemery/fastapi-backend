"""
Routes package
"""

from routes.auth import router as auth_router

from fastapi import APIRouter
router = APIRouter()
router.include_router(auth_router)

__all__ = ["router"]