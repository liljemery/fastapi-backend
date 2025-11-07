"""
Centralized logging configuration

"""
import logging
import sys
import json
from datetime import datetime
from typing import Any, Dict
from config import settings


class JSONFormatter(logging.Formatter):
    """
    JSON formatter for structured logging
    
    """
    
    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        for key, value in record.__dict__.items():
            if key not in [
                "name", "msg", "args", "created", "filename", "funcName",
                "levelname", "levelno", "lineno", "module", "msecs",
                "message", "pathname", "process", "processName", "relativeCreated",
                "thread", "threadName", "exc_info", "exc_text", "stack_info",
                "request_id", "user_id"
            ]:
                log_data[key] = value
        
        return json.dumps(log_data)


class ColoredFormatter(logging.Formatter):
    """
    Colored formatter for development
    
    """
    
    COLORS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[35m",  # Magenta
        "RESET": "\033[0m",      # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        reset = self.COLORS["RESET"]
        
        log_message = (
            f"{color}[{datetime.utcnow().strftime('%H:%M:%S')}] "
            f"{record.levelname:8s}{reset} "
            f"[{record.name}] {record.getMessage()}"
        )
        
        if record.exc_info:
            log_message += f"\n{self.formatException(record.exc_info)}"
        
        return log_message


def setup_logging() -> None:
    """
    Configure application logging
    
    """
    
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    root_logger.handlers.clear()
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    formatter: logging.Formatter
    if settings.ENVIRONMENT == "production":
        formatter = JSONFormatter()
    else:
        formatter = ColoredFormatter()
    
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Silence noisy third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    
    # Log the logging configuration
    logger = logging.getLogger(__name__)
    logger.info(
        f"Logging configured: level={settings.LOG_LEVEL}, "
        f"environment={settings.ENVIRONMENT}"
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance
    
    USAGE:
        from utils.logging_config import get_logger
        logger = get_logger(__name__)
        logger.info("Something happened")
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


SENSITIVE_PATTERNS = [
    "password",
    "token",
    "secret",
    "api_key",
    "authorization",
    "credit_card",
    "ssn",
]


def sanitize_log_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove sensitive data from log entries
    
    Args:
        data: Dictionary potentially containing sensitive data
    
    Returns:
        Sanitized dictionary with sensitive values masked
    """
    sanitized: Dict[str, Any] = {}
    
    for key, value in data.items():
        key_lower = key.lower()
        
        is_sensitive = any(pattern in key_lower for pattern in SENSITIVE_PATTERNS)
        
        if is_sensitive:
            sanitized[key] = "***REDACTED***"
        elif isinstance(value, dict):
            sanitized[key] = sanitize_log_data(value)
        else:
            sanitized[key] = value
    
    return sanitized

