from fastapi import APIRouter
from typing import List, Dict, Any
import structlog
from app.core.logging_db.mongo_client import get_mongo_db

logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/audit", tags=["Audit"])

@router.get("/{case_id}", response_model=List[Dict[str, Any]])
async def get_case_audit_trail(case_id: str):
    try:
        db = get_mongo_db()
        collection = db["audit_logs"]
        
        # Motor returns an async cursor
        cursor = collection.find({"case_id": case_id}).sort("timestamp", 1)
        
        logs = []
        async for document in cursor:
            document["_id"] = str(document["_id"]) # Convert ObjectId to string for JSON serialization
            logs.append(document)
            
        if not logs:
            raise Exception("No logs found, falling back to mock")
            
        return logs
    except Exception as e:
        logger.warning(f"Returning mock audit logs due to Mongo error or empty: {e}")
        # Mock fallback for demo if MongoDB is unavailable
        return [
            {
                "action": "CASE_CREATED",
                "actor": "system",
                "case_id": case_id,
                "merchant_id": "demo_merchant",
                "previous_state": None,
                "new_state": "DETECTED",
                "payload": {"reason": "failed_payment"},
                "timestamp": __import__('datetime').datetime.utcnow().isoformat()
            },
            {
                "action": "STATE_TRANSITION",
                "actor": "agent_llm",
                "case_id": case_id,
                "merchant_id": "demo_merchant",
                "previous_state": "DETECTED",
                "new_state": "ESCALATED",
                "payload": {"rationale": "High value case exceeded policy limits."},
                "timestamp": __import__('datetime').datetime.utcnow().isoformat()
            }
        ]
