"""
Request ID middleware

Adds unique request ID to each request for distributed tracing
"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import uuid


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Add unique request ID to each request for tracing
    
    WHY:
    - Track requests through entire system
    - Debug issues in production
    - Correlate errors across services
    - Essential for distributed systems
    """
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Add to response headers for client-side debugging
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

