"""
Dashboard request/response schemas

Pydantic models for dashboard endpoints
"""
from pydantic import BaseModel
from typing import Optional


class DashboardResponse(BaseModel):
    """Dashboard data response"""
    id: int
    uuid: str
    email: str
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    is_admin: bool
    is_verified: bool
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True

