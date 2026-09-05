from typing import Dict, Any
from app.events.bus import event_bus
from app.core.db.session import get_db_session
from app.recovery.repository import RecoveryCaseRepository
from app.recovery.orchestrator import RecoveryOrchestrator
from app.agent.service import AgentService
from app.policies.rules.chain import PolicyEngine
from app.razorpay_client.client import RazorpayClient
from app.notifications.dispatcher import NotificationDispatcher
import structlog

logger = structlog.get_logger(__name__)

async def process_anomaly_event(payload: Dict[str, Any]):
    """
    Subscribes to anomaly events and triggers the recovery orchestrator.
    """
    try:
        # get_db_session is an async generator
        async for session in get_db_session():
            case_repo = RecoveryCaseRepository(session)
            agent_service = AgentService()
            policy_engine = PolicyEngine()
            razorpay_client = RazorpayClient()
            notifier = NotificationDispatcher()
            
            orchestrator = RecoveryOrchestrator(
                case_repo=case_repo,
                agent_service=agent_service,
                policy_engine=policy_engine,
                razorpay_client=razorpay_client,
                notification_dispatcher=notifier
            )
            
            event_type = payload.get("type", "unknown")
            await orchestrator.handle_event(event_type, payload)
            
            # Break after executing with one session
            break
    except Exception as e:
        logger.error("anomaly_event_processing_failed", error=str(e), payload=payload)

def setup_subscribers():
    logger.info("Setting up event bus subscribers...")
    event_bus.subscribe("revenue.anomaly.product", process_anomaly_event)
    event_bus.subscribe("revenue.anomaly.txn_volume", process_anomaly_event)
    event_bus.subscribe("churn.activity_drop", process_anomaly_event)
    event_bus.subscribe("premium.payment.failed", process_anomaly_event)
