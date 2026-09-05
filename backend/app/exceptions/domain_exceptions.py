from .base import AppException

class DomainException(AppException):
    """Base exception for domain-level errors."""
    def __init__(self, message: str, error_code: str = "DOMAIN_ERROR", status_code: int = 400, **kwargs):
        super().__init__(message, error_code, status_code, **kwargs)

class PaymentNotFoundError(DomainException):
    def __init__(self, payment_id: str):
        super().__init__(f"Payment with ID {payment_id} not found", error_code="PAYMENT_NOT_FOUND", status_code=404, payment_id=payment_id)

class OrderNotFoundError(DomainException):
    def __init__(self, order_id: str):
        super().__init__(f"Order with ID {order_id} not found", error_code="ORDER_NOT_FOUND", status_code=404, order_id=order_id)

class SubscriptionNotFoundError(DomainException):
    def __init__(self, subscription_id: str):
        super().__init__(f"Subscription with ID {subscription_id} not found", error_code="SUBSCRIPTION_NOT_FOUND", status_code=404, subscription_id=subscription_id)

class InvalidCaseStateTransitionError(DomainException):
    def __init__(self, from_state: str, to_state: str):
        super().__init__(f"Invalid state transition from {from_state} to {to_state}", error_code="INVALID_STATE_TRANSITION", status_code=409)

class DuplicateEventError(DomainException):
    def __init__(self, event_id: str):
        super().__init__(f"Duplicate event with ID {event_id}", error_code="DUPLICATE_EVENT", status_code=409)
