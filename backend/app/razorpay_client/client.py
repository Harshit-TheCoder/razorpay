import razorpay
from typing import Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from app.core.config import get_settings
from .schemas import RazorpayExecutionResponse
import structlog

logger = structlog.get_logger(__name__)
settings = get_settings()

class RazorpayClient:
    def __init__(self):
        # We assume the merchant's key is passed in dynamically for multi-tenancy,
        # but for this skeleton we fall back to a system-wide sandbox key if available.
        # Ensure we don't crash if keys are missing in the env.
        key_id = settings.RAZORPAY_KEY_ID or "rzp_test_stub"
        key_secret = settings.RAZORPAY_KEY_SECRET or "stub_secret"
        self.client = razorpay.Client(auth=(key_id, key_secret))

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(Exception) # In production, narrow this to Network errors
    )
    async def _execute_with_retry(self, func, *args, **kwargs):
        # Since razorpay official SDK is sync, we might need to run it in a threadpool
        # in a true async app. For the skeleton, we wrap the sync call natively.
        return func(*args, **kwargs)

    async def execute_action(self, action_type: str, payload: Dict[str, Any]) -> RazorpayExecutionResponse:
        logger.info(f"Executing Razorpay action: {action_type}", payload=payload)
        
        try:
            if action_type == "retry_payment":
                # Real SDK call to capture
                # In sandbox, payment ID could be missing or invalid. Razorpay might throw an error.
                payment_id = payload.get("payment_id")
                amount = payload.get("amount", 1000) # Amount in paise (e.g. 10.00 INR)
                if not payment_id:
                    return RazorpayExecutionResponse(success=False, raw_response={}, error_message="Missing payment_id")
                
                resp = await self._execute_with_retry(self.client.payment.capture, payment_id, amount)
                return RazorpayExecutionResponse(success=True, raw_response=resp)
                
            elif action_type == "create_payment_link":
                # Real SDK call to create payment link
                link_payload = {
                    "amount": payload.get("amount", 1000),
                    "currency": "INR",
                    "accept_partial": False,
                    "description": payload.get("description", "Payment recovery"),
                    "customer": {
                        "name": payload.get("customer_name", "Customer"),
                        "email": payload.get("customer_email", "customer@example.com"),
                        "contact": payload.get("customer_phone", "+919999999999")
                    },
                    "notify": {
                        "sms": True,
                        "email": True
                    },
                    "reminder_enable": True
                }
                resp = await self._execute_with_retry(self.client.payment_link.create, link_payload)
                return RazorpayExecutionResponse(success=True, raw_response=resp)
                
            else:
                # Default fallback for unmapped actions
                return RazorpayExecutionResponse(success=True, raw_response={"status": "executed_stub", "action": action_type})
                
        except Exception as e:
            logger.error(f"Razorpay execution failed: {str(e)}")
            return RazorpayExecutionResponse(success=False, raw_response={}, error_message=str(e))
