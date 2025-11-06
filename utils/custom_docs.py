from typing import Any
from fastapi import FastAPI  # type: ignore[import-untyped]
from fastapi.openapi.utils import get_openapi  # type: ignore[import-untyped]

def custom_openapi(app: FastAPI) -> dict[str, Any]:
    """Custom OpenAPI schema for the FastAPI application"""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Base Fastapi Backend API", 
        version="0.0.1",
        description="Base Fastapi Backend API to serve requests to the Base Fastapi Backend",
        routes=app.routes,
    )
    
    # Ensure components exist
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    
    # Add security scheme for Bearer token (FastAPI HTTPBearer compatible)
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "token",
            "description": "Enter your authentication token"
        }
    }
    
    # Add security requirements to protected endpoints
    for path in openapi_schema["paths"]:
        # Check if this path has any operations
        if not openapi_schema["paths"][path]:
            continue
            
        # Apply security to all operations in protected paths
        for method in openapi_schema["paths"][path]:
            if method.lower() in ["get", "post", "put", "delete"]:
                # Skip auth endpoints (login, register)
                if "/auth/login" in path or "/auth/register" in path:
                    continue
                    
                # Apply security to all other endpoints
                openapi_schema["paths"][path][method]["security"] = [{"HTTPBearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema