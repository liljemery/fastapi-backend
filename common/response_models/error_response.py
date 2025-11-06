"""
Error response models
"""
from pydantic import BaseModel
from typing import Optional, Any, Dict, Union, cast


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


def generate_error_response_for_statuses(status_codes: list[int]) -> Dict[Union[int, str], Dict[str, Any]]:
    """
    Generate error response schemas for specified status codes
    
    Args:
        status_codes: List of HTTP status codes
        
    Returns:
        Dictionary mapping status codes to error response schemas
    """
    responses: Dict[Union[int, str], Dict[str, Any]] = {}
    for status_code in status_codes:
        responses[status_code] = {
            "model": ErrorResponse,
            "description": f"Error response for status {status_code}"
        }
    return cast(Dict[Union[int, str], Dict[str, Any]], responses)

