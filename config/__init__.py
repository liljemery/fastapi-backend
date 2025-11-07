"""
Configuration module for application settings

"""
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List
import os
import secrets
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """
    Application settings with production-grade configuration
    
    - Automatic environment variable parsing
    - Type validation at startup (fail fast)
    - Clear documentation of required vs optional
    - Easy testing with overrides
    """
    
    # ==================== Application ====================
    APP_NAME: str = Field(
        default="FastAPI Backend API",
        description="Application name"
    )
    APP_VERSION: str = Field(
        default="1.0.0",
        description="Application version"
    )
    DEBUG: bool = Field(
        default=False,
        description="Debug mode - disable in production"
    )
    ENVIRONMENT: str = Field(
        default="development",
        description="Environment: development, staging, production"
    )
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL"
    )
    
    # ==================== Database ====================
    DATABASE_URL: str = Field(
        default="sqlite:///./test.db",
        description="Database connection URL"
    )
    
    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Warn if using SQLite in production"""
        if os.getenv("ENVIRONMENT") == "production" and "sqlite" in v:
            import warnings
            warnings.warn("SQLite detected in production - use PostgreSQL for production workloads")
        return v
    
    # ==================== Security ====================
    SECRET_KEY: str = Field(
        default_factory=lambda: os.getenv("SECRET_KEY") or secrets.token_urlsafe(32),
        description="JWT secret key - MUST be set in production"
    )
    ALGORITHM: str = Field(
        default="HS256",
        description="JWT signing algorithm"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="Access token expiration time in minutes"
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7,
        description="Refresh token expiration time in days"
    )
    
    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Ensure secret key is strong enough in production"""
        if os.getenv("ENVIRONMENT") == "production" and len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters in production")
        return v
    
    # ==================== CORS ====================
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins"
    )
    
    @field_validator("CORS_ORIGINS")
    @classmethod
    def validate_cors_origins(cls, v: List[str]) -> List[str]:
        """Warn about wildcard CORS in production"""
        if os.getenv("ENVIRONMENT") == "production" and "*" in v:
            import warnings
            warnings.warn("Wildcard CORS origins detected in production - specify exact domains")
        return v
    
    # ==================== Encryption ====================
    ENCRYPTION_SALT: str = Field(
        default_factory=lambda: os.getenv("ENCRYPTION_SALT") or secrets.token_hex(16),
        description="Salt for encryption operations"
    )
    INIT_VECTOR: str = Field(
        default_factory=lambda: os.getenv("INIT_VECTOR") or secrets.token_hex(16),
        description="Initialization vector for encryption"
    )
    
    # ==================== Email (Consolidated) ====================
    EMAIL_HOST: str = Field(
        default="smtp.gmail.com",
        description="SMTP server hostname"
    )
    EMAIL_PORT: int = Field(
        default=587,
        description="SMTP server port (587 for TLS, 465 for SSL)"
    )
    EMAIL_USER: Optional[str] = Field(
        default=None,
        description="SMTP username"
    )
    EMAIL_PASSWORD: Optional[str] = Field(
        default=None,
        description="SMTP password"
    )
    EMAIL_FROM: str = Field(
        default="noreply@example.com",
        description="Default from email address"
    )
    EMAIL_FROM_NAME: str = Field(
        default="FastAPI Backend",
        description="Default from name"
    )
    EMAIL_USE_TLS: bool = Field(
        default=True,
        description="Use TLS for email"
    )
    
    # Legacy SMTP aliases for backward compatibility
    @property
    def SMTP_HOST(self) -> str:
        """Legacy alias for EMAIL_HOST"""
        return self.EMAIL_HOST
    
    @property
    def SMTP_PORT(self) -> int:
        """Legacy alias for EMAIL_PORT"""
        return self.EMAIL_PORT
    
    @property
    def SMTP_USER(self) -> Optional[str]:
        """Legacy alias for EMAIL_USER"""
        return self.EMAIL_USER
    
    @property
    def SMTP_PASSWORD(self) -> Optional[str]:
        """Legacy alias for EMAIL_PASSWORD"""
        return self.EMAIL_PASSWORD
    
    # ==================== Rate Limiting ====================
    RATE_LIMIT_ENABLED: bool = Field(
        default=True,
        description="Enable rate limiting"
    )
    RATE_LIMIT_PER_MINUTE: int = Field(
        default=60,
        description="Max requests per minute per IP"
    )
    
    # ==================== Configuration ====================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()

general_config = settings

