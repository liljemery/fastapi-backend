"""
Application factory for creating FastAPI app instance

Orchestrates middleware stack, route registration, and lifecycle management
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from utils.custom_docs import custom_openapi
from contextlib import asynccontextmanager
from routes import router as routes_router
from config import settings
from database import init_db, close_db
from middlewares import (
    exception_handler_middleware,
    RequestIDMiddleware,
    LoggingMiddleware
)
import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    
    WHY:
    - Proper resource initialization and cleanup
    - Prevents connection leaks
    - Graceful shutdown important for containers/K8s
    """
    logger.info("Starting up application...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    init_db()
    logger.info("Database initialized")
    
    yield
    
    logger.info("Shutting down application...")
    await close_db()
    logger.info("Database connections closed")


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application
    
    Returns:
        FastAPI: Configured application instance
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan,
        docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
        redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
    )
    
    # ==================== Middleware Stack ====================
    
    app.add_middleware(RequestIDMiddleware)
    
    app.add_middleware(LoggingMiddleware)
    
    app.middleware("http")(exception_handler_middleware)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    if settings.ENVIRONMENT == "production":
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["*.yourdomain.com", "yourdomain.com"]
        )
    
    # ==================== Routes ====================
    register_routes(app)
    
    # ==================== OpenAPI ====================
    if settings.ENVIRONMENT != "production":
        app.openapi_schema = custom_openapi(app)
    
    logger.info("Application created successfully")
    return app


def register_routes(app: FastAPI) -> None:
    """
    Register all application routes
    
    """
    app.include_router(routes_router)
    
    @app.get("/health", tags=["System"])
    async def health_check():
        """Health check for load balancers and K8s probes"""
        return {
            "status": "healthy",
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT
        }
    
    @app.get("/", tags=["System"])
    async def root():
        """API information endpoint"""
        return {
            "message": f"Welcome to {settings.APP_NAME}",
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
            "docs": "/docs" if settings.ENVIRONMENT != "production" else "disabled"
        }

