import functools
import structlog
from app.audit.schemas import AuditLogEntry
from app.audit.service import AuditService

logger = structlog.get_logger(__name__)

def audit_log(action_name: str):
    """
    Decorator to wrap orchestrator or service methods and automatically log their execution.
    It attempts to extract `merchant_id` and `case_id` if present in kwargs.
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Execute the actual function
            result = await func(*args, **kwargs)
            
            # Post-execution audit logging (fire-and-forget logic could be used here)
            try:
                # Naively try to extract standard IDs from kwargs or the result object
                merchant_id = kwargs.get("merchant_id") or getattr(result, "merchant_id", None)
                case_id = kwargs.get("case_id") or getattr(result, "id", None)
                new_state = getattr(result, "state", None)

                entry = AuditLogEntry(
                    action=action_name,
                    merchant_id=merchant_id,
                    case_id=case_id,
                    new_state=new_state,
                    payload={"kwargs": str(kwargs)} # Naive serialization for skeleton
                )
                
                await AuditService.log_action(entry)
            except Exception as e:
                logger.error("Audit decorator failed to log", error=str(e))
                
            return result
        return wrapper
    return decorator
