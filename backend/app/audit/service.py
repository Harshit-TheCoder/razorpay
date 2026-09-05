from typing import Any
import structlog
from app.audit.schemas import AuditLogEntry
from app.core.logging_db.mongo_client import get_mongo_db

logger = structlog.get_logger(__name__)

class AuditService:
    @staticmethod
    async def log_action(entry: AuditLogEntry) -> None:
        try:
            db = get_mongo_db()
            collection = db["audit_logs"]
            
            # Motor operates asynchronously
            document = entry.model_dump()
            await collection.insert_one(document)
            logger.debug("Audit log inserted successfully", action=entry.action)
        except Exception as e:
            # Audit failures shouldn't bring down the main workflow, but must be alerted
            logger.error("Failed to write to audit log", error=str(e), action=entry.action)
