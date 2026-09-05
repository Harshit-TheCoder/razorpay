class AppException(Exception):
    """Base exception for all custom application errors."""
    
    def __init__(self, message: str, error_code: str = "INTERNAL_ERROR", status_code: int = 500, **kwargs):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.kwargs = kwargs
