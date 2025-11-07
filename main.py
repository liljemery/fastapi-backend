"""
Main application entry point for FastAPI Backend Template
"""
from utils.app_factory import create_app
from utils.logging_config import setup_logging
from config import settings

setup_logging()

app = create_app()

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(settings.__dict__.get("PORT", 8000)),
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=settings.DEBUG,
        workers=1 if settings.DEBUG else 4,
        loop="uvloop",
        http="httptools",
    )

