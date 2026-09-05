import asyncio
import structlog
import uuid
from datetime import datetime
from app.events.bus import event_bus

logger = structlog.get_logger(__name__)

async def detect_anomalies_loop():
    """
    Background job that periodically scans for anomalies and publishes events.
    In a real system, this would query the DB for metrics.
    For this skeleton, it periodically emits synthetic anomaly events.
    """
    logger.info("Starting anomaly detector background job...")
    while True:
        await asyncio.sleep(60) # Run every 60 seconds
        
        # Simulate detecting a revenue drop
        revenue_drop_payload = {
            "merchant_id": "demo_merchant",
            "source_ref": f"anomaly_rev_{uuid.uuid4().hex[:8]}",
            "type": "revenue_drop",
            "timestamp": datetime.utcnow().isoformat()
        }
        await event_bus.publish("revenue.anomaly.product", revenue_drop_payload)
        logger.info("Published synthetic revenue_drop anomaly")
        
        # Simulate detecting a volume drop
        volume_drop_payload = {
            "merchant_id": "demo_merchant",
            "source_ref": f"anomaly_vol_{uuid.uuid4().hex[:8]}",
            "type": "volume_drop",
            "timestamp": datetime.utcnow().isoformat()
        }
        await event_bus.publish("revenue.anomaly.txn_volume", volume_drop_payload)
        logger.info("Published synthetic volume_drop anomaly")
