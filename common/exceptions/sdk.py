"""
SDK-specific exceptions
"""
from typing import Optional, Dict, Any


class SDKException(Exception):
    """
    Base exception for SDK operations
    """
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}
        super().__init__(self.message)


class SDKConnectionError(SDKException):
    """Raised when unable to connect to external service"""
    def __init__(self, message: str = "Failed to connect to external service", **kwargs):
        super().__init__(message, **kwargs)


class SDKTimeoutError(SDKException):
    """Raised when request times out"""
    def __init__(self, message: str = "Request timed out", **kwargs):
        super().__init__(message, **kwargs)


class SDKHTTPError(SDKException):
    """Raised when receiving non-2xx HTTP response"""
    def __init__(self, message: str, status_code: int, response_data: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=status_code, response_data=response_data)


class SDKValidationError(SDKException):
    """Raised when request/response validation fails"""
    def __init__(self, message: str = "Validation error", **kwargs):
        super().__init__(message, **kwargs)


class SDKResourceNotFoundError(SDKException):
    """Raised when requested resource is not found"""
    def __init__(self, message: str = "Resource not found", **kwargs):
        super().__init__(message, status_code=404, **kwargs)


class SDKUnauthorizedError(SDKException):
    """Raised when authentication fails"""
    def __init__(self, message: str = "Unauthorized", **kwargs):
        super().__init__(message, status_code=401, **kwargs)

