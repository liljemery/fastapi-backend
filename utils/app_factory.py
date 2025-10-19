"""
Application factory for creating FastAPI app instance
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routes import router as routes_router
from config import settings
from database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    print("Starting up application...")
    init_db()
    yield
    # Shutdown
    print("Shutting down application...")


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
        lifespan=lifespan
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Register routes
    register_routes(app)
    
    return app


def register_routes(app: FastAPI):
    """Register all application routes"""
    app.include_router(routes_router)
    # Health check
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "version": settings.APP_VERSION}
    
    @app.get("/")
    async def root():
        return {
            "message": "Welcome to Foodvery Backend API",
            "version": settings.APP_VERSION,
            "docs": "/docs"
        }
    
