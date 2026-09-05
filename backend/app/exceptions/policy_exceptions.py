from .base import AppException

class PolicyException(AppException):
    def __init__(self, message: str, error_code: str = "POLICY_VIOLATION", status_code: int = 422, **kwargs):
        super().__init__(message, error_code, status_code, **kwargs)

class PolicyViolationError(PolicyException):
    pass
