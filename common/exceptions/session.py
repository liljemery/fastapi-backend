"""
Session-specific exceptions
"""


class NoSessionError(Exception):
    """Raised when session is not available"""
    
    def __init__(self, message: str = "No session available"):
        self.message = message
        super().__init__(self.message)

