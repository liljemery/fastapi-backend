"""
Dashboard-specific exceptions
"""


class UserNotFoundError(Exception):
    """Raised when user is not found"""
    
    def __init__(self, message: str = "User not found"):
        self.message = message
        super().__init__(self.message)


class DashboardError(Exception):
    """Base exception for dashboard errors"""
    
    def __init__(self, message: str = "Dashboard error"):
        self.message = message
        super().__init__(self.message)

