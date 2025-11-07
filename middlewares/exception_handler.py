"""
Global exception handler middleware
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
from typing import Any, Dict

from common.exceptions.auth import AuthException
from common.exceptions.sdk import SDKException
from config import settings

logger = logging.getLogger(__name__)


async def exception_handler_middleware(request: Request, call_next):
    """
    Global exception handler middleware
    """
    try:
        return await call_next(request)
    except Exception as exc:
        return await handle_exception(request, exc)


async def handle_exception(request: Request, exc: Exception) -> JSONResponse:
    """
    Convert exceptions to JSON responses
    
    PRIORITY ORDER:
    1. Custom business exceptions (AuthException, SDKException)
    2. FastAPI validation errors (422)
    3. Starlette HTTP exceptions
    4. Unexpected errors (500)
    """
    
    request_context = {
        "method": request.method,
        "url": str(request.url),
        "client": request.client.host if request.client else "unknown",
    }
    
    # Handle custom auth exceptions
    if isinstance(exc, AuthException):
        logger.warning(
            f"Auth error: {exc.message}",
            extra={"exception": exc, **request_context}
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "authentication_error",
                "message": exc.message,
                "status_code": exc.status_code
            }
        )
    
    # Handle SDK exceptions
    if isinstance(exc, SDKException):
        logger.error(
            f"SDK error: {exc.message}",
            extra={"exception": exc, **request_context}
        )
        return JSONResponse(
            status_code=exc.status_code or 500,
            content={
                "error": "external_service_error",
                "message": exc.message,
                "status_code": exc.status_code or 500,
                "details": exc.response_data if settings.DEBUG else None
            }
        )
    
    # Handle FastAPI validation errors
    if isinstance(exc, RequestValidationError):
        logger.warning(
            f"Validation error: {exc.errors()}",
            extra={"errors": exc.errors(), **request_context}
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "validation_error",
                "message": "Invalid request data",
                "details": exc.errors() if settings.DEBUG else None,
                "status_code": 422
            }
        )
    
    # Handle Starlette HTTP exceptions
    if isinstance(exc, StarletteHTTPException):
        logger.warning(
            f"HTTP error {exc.status_code}: {exc.detail}",
            extra={"exception": exc, **request_context}
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "http_error",
                "message": exc.detail,
                "status_code": exc.status_code
            }
        )
    
    # Handle unexpected errors
    logger.error(
        f"Unexpected error: {str(exc)}",
        exc_info=True,  # Include stack trace in logs
        extra={"exception": exc, **request_context}
    )
    
    # In production, never expose internal error details
    if settings.ENVIRONMENT == "production":
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "internal_server_error",
                "message": "An unexpected error occurred. Please try again later.",
                "status_code": 500
            }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "internal_server_error",
                "message": str(exc),
                "type": type(exc).__name__,
                "status_code": 500
            }
        )


def format_error_response(
    error_type: str,
    message: str,
    status_code: int = 400,
    details: Any = None
) -> Dict[str, Any]:
    """
    Format error response consistently
    
    """
    response = {
        "error": error_type,
        "message": message,
        "status_code": status_code
    }
    
    if details is not None:
        response["details"] = details
    
    return response

