"""
Error response models
"""
from pydantic import BaseModel
from typing import Optional, Any


class ErrorResponse(BaseModel):
    """Standard error response"""
    
    error: str
    message: str
    details: Optional[Any] = None
    status_code: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Invalid input data",
                "details": {"field": "email", "issue": "Invalid email format"},
                "status_code": 400
            }
        }

