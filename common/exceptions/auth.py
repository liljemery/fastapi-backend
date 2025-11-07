"""
Authentication-specific exceptions

REFACTOR NOTES:
- Consolidated auth exceptions from multiple locations
- Each exception carries HTTP status code for consistent responses
- More specific exceptions than generic HTTPException
"""
from typing import Optional


class AuthException(Exception):
    """Base exception for authentication errors"""
    def __init__(self, message: str, status_code: int = 401):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class InvalidCredentialsException(AuthException):
    """Raised when login credentials are invalid"""
    def __init__(self, message: str = "Invalid email or password"):
        super().__init__(message, status_code=401)


class UserNotFoundException(AuthException):
    """Raised when user is not found"""
    def __init__(self, message: str = "User not found", identifier: Optional[str] = None):
        if identifier:
            message = f"{message}: {identifier}"
        super().__init__(message, status_code=404)


class UserAlreadyExistsException(AuthException):
    """Raised when attempting to create user with existing email/username"""
    def __init__(self, message: str = "User already exists", field: Optional[str] = None):
        if field:
            message = f"User with this {field} already exists"
        super().__init__(message, status_code=409)


class InvalidTokenException(AuthException):
    """Raised when JWT token is invalid or expired"""
    def __init__(self, message: str = "Invalid or expired token"):
        super().__init__(message, status_code=401)


class UnauthorizedException(AuthException):
    """Raised when user lacks required permissions"""
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message, status_code=403)


class EmailNotVerifiedException(AuthException):
    """Raised when user hasn't verified their email"""
    def __init__(self, message: str = "Email not verified"):
        super().__init__(message, status_code=403)


class AccountInactiveException(AuthException):
    """Raised when user account is inactive"""
    def __init__(self, message: str = "Account is inactive"):
        super().__init__(message, status_code=403)

