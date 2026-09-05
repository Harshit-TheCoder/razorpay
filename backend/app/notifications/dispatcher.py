import structlog
import uuid
from typing import Optional
from .schemas import NotificationPayload, NotificationResult
from .templates import TEMPLATES

logger = structlog.get_logger(__name__)

class NotificationDispatcher:
    def __init__(self):
        # In a real app: initialize twilio/sendgrid SDKs here
        pass

    async def dispatch(self, payload: NotificationPayload) -> NotificationResult:
        template = TEMPLATES.get(payload.template_id)
        if not template:
            logger.error("Template not found", template_id=payload.template_id)
            return NotificationResult(success=False, error="Template not found")

        # Mocking dispatch by writing to a log file
        try:
            # Safely format the template body with provided context data
            body_text = template["body"]
            
            class SafeDict(dict):
                def __missing__(self, key):
                    return "{" + key + "}"
                    
            import string
            formatter = string.Formatter()
            rendered_body = formatter.vformat(body_text, (), SafeDict(payload.context_data))

            log_entry = (
                f"--- NOTIFICATION DISPATCH ---\n"
                f"ID: {uuid.uuid4()}\n"
                f"To: {payload.customer_id}\n"
                f"Channel: {payload.channel}\n"
                f"Template: {payload.template_id}\n"
                f"Subject: {template.get('subject', 'No Subject')}\n"
                f"Body:\n{rendered_body}\n"
                f"-----------------------------\n\n"
            )
            
            with open("notifications.log", "a") as f:
                f.write(log_entry)
                
            logger.info("Notification dispatched to notifications.log", channel=payload.channel, template_id=payload.template_id)
        except Exception as e:
            logger.error("Failed to mock dispatch notification", error=str(e))
            return NotificationResult(success=False, error=str(e))
        
        return NotificationResult(success=True, message_id=str(uuid.uuid4()))
