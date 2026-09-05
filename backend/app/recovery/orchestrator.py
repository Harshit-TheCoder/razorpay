import structlog
from typing import Dict, Any
from app.recovery.repository import RecoveryCaseRepository
from app.recovery.models import RecoveryCase, RecoveryAttempt
from app.recovery.case_state_machine import CaseStateMachine, CaseState
from app.agent.service import AgentService
from app.policies.rules.chain import PolicyEngine
from app.razorpay_client.client import RazorpayClient
from app.notifications.dispatcher import NotificationDispatcher
from app.notifications.schemas import NotificationPayload
from app.audit.decorators import audit_log
from app.exceptions.domain_exceptions import InvalidCaseStateTransitionError
from app.exceptions.policy_exceptions import PolicyViolationError

logger = structlog.get_logger(__name__)

class RecoveryOrchestrator:
    def __init__(
        self,
        case_repo: RecoveryCaseRepository,
        agent_service: AgentService,
        policy_engine: PolicyEngine,
        razorpay_client: RazorpayClient,
        notification_dispatcher: NotificationDispatcher
    ):
        self.case_repo = case_repo
        self.agent = agent_service
        self.policy = policy_engine
        self.razorpay = razorpay_client
        self.notifier = notification_dispatcher
        self.state_machine = CaseStateMachine()

    @audit_log(action_name="process_recovery_event")
    async def handle_event(self, event_type: str, payload: Dict[str, Any]) -> RecoveryCase:
        # Step 1: Context & Creation
        merchant_id = payload.get("merchant_id", "default")
        source_ref = payload.get("source_ref", "unknown")
        
        # Map event types to scenario types for the agent
        event_to_scenario = {
            "payment.failed": "failed_payment",
            "checkout.abandoned": "checkout_abandonment",
            "subscription.charge.failed": "subscription_recovery",
            "premium.payment.failed": "premium_recovery",
            "revenue.anomaly.product": "revenue_drop",
            "revenue.anomaly.txn_volume": "volume_drop",
            "churn.activity_drop": "churn_recovery",
        }
        
        scenario_type = event_to_scenario.get(event_type, "failed_payment") # Fallback to generic failed_payment
        
        import random
        amount = payload.get("amount", random.randint(50000, 1500000))
        
        case = RecoveryCase(
            merchant_id=merchant_id,
            scenario_type=scenario_type,
            source_ref=source_ref,
            amount=amount,
            state=CaseState.DETECTED
        )
        case = await self.case_repo.create(case)
        
        # Publish Domain Event for Saga Coordinator to pick up
        from app.events.bus import event_bus
        await event_bus.publish("recovery.case.created", {
            "case_id": case.id,
            "original_payload": payload
        })
        
        logger.info("Published recovery.case.created", case_id=case.id)
        return case
