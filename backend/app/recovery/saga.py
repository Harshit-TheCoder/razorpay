import structlog
from typing import Dict, Any
from app.events.bus import event_bus
from app.core.db.session import get_db_session
from app.recovery.repository import RecoveryCaseRepository
from app.recovery.case_state_machine import CaseStateMachine, CaseState
from app.agent.service import AgentService
from app.policies.rules.chain import PolicyEngine
from app.razorpay_client.client import RazorpayClient
from app.notifications.dispatcher import NotificationDispatcher
from app.notifications.schemas import NotificationPayload
from app.exceptions.policy_exceptions import PolicyViolationError
from app.core.idempotency import acquire_idempotency_key, IdempotencyConflictError
from app.recovery.schemas import ActionProposal

logger = structlog.get_logger(__name__)
state_machine = CaseStateMachine()

async def handle_case_created(payload: Dict[str, Any]):
    """Handles the event when a new case is detected."""
    case_id = payload.get("case_id")
    if not case_id:
        return
        
    logger.info("Saga: processing case created", case_id=case_id)
    try:
        async for session in get_db_session():
            repo = RecoveryCaseRepository(session)
            case = await repo.get(case_id)
            if not case:
                return
            
            # Transition to INVESTIGATING
            case.state = state_machine.transition(case.state, CaseState.INVESTIGATING)
            case = await repo.update(case.id, case)
            
            # Run Agent
            agent_service = AgentService()
            action_proposal = await agent_service.run(case.scenario_type, {"case_id": case.id, "payload": payload.get("original_payload")})
            
            # Transition to PROPOSED
            case.state = state_machine.transition(case.state, CaseState.DIAGNOSED)
            case.state = state_machine.transition(case.state, CaseState.ACTION_PROPOSED)
            case = await repo.update(case.id, case)
            
            # Publish Next Event
            await event_bus.publish("recovery.action.proposed", {
                "case_id": case.id,
                "merchant_id": case.merchant_id,
                "action_type": action_proposal.action_type,
                "action_payload": action_proposal.payload
            })
            break
    except Exception as e:
        logger.error("Saga step failed: handle_case_created", case_id=case_id, error=str(e))
        try:
            async for session in get_db_session():
                repo = RecoveryCaseRepository(session)
                case = await repo.get(case_id)
                case.state = state_machine.transition(case.state, CaseState.ESCALATED)
                await repo.update(case.id, case)
                break
        except Exception as update_err:
            logger.error("Failed to escalate case after agent crash", case_id=case_id, error=str(update_err))

async def handle_action_proposed(payload: Dict[str, Any]):
    """Handles the event to execute the proposed action."""
    case_id = payload.get("case_id")
    merchant_id = payload.get("merchant_id")
    action_type = payload.get("action_type")
    action_payload = payload.get("action_payload")
    
    if not case_id:
        return
        
    logger.info("Saga: processing action proposed", case_id=case_id)
    try:
        async for session in get_db_session():
            repo = RecoveryCaseRepository(session)
            case = await repo.get(case_id)
            
            # Transition to POLICY_CHECK
            case.state = state_machine.transition(case.state, CaseState.POLICY_CHECK)
            case = await repo.update(case.id, case)
            
            if action_type == "escalate":
                logger.info("AI Agent explicitly escalated case", case_id=case_id)
                case.state = state_machine.transition(case.state, CaseState.ESCALATED)
                await repo.update(case.id, case)
                return
                
            policy_engine = PolicyEngine()
            # ActionProposal mock for policy engine
            action_prop = ActionProposal(action_type=action_type, payload=action_payload)
            is_allowed = await policy_engine.evaluate(merchant_id, action_prop)
            if not is_allowed:
                raise PolicyViolationError("Action blocked by policy")
                
            # Idempotency
            idempotency_key = f"{case.id}:attempt_1:{action_type}"
            if not await acquire_idempotency_key(idempotency_key):
                raise IdempotencyConflictError(f"Action already executed for {idempotency_key}")
                
            # Execution
            if action_type in ["send_email", "send_sms"]:
                notifier = NotificationDispatcher()
                notif_payload = NotificationPayload(
                    customer_id=action_payload.get("customer_id", "unknown"),
                    template_id=action_payload.get("template_id", "default"),
                    context_data=action_payload,
                    channel="email" if action_type == "send_email" else "sms"
                )
                await notifier.dispatch(notif_payload)
            else:
                razorpay_client = RazorpayClient()
                await razorpay_client.execute_action(action_type, action_payload)
                
            # Transition to EXECUTED
            case.state = state_machine.transition(case.state, CaseState.ACTION_EXECUTED)
            case = await repo.update(case.id, case)
            
            await event_bus.publish("recovery.action.executed", {"case_id": case.id})
            break
            
    except PolicyViolationError as e:
        logger.warning("policy_violation in saga", case_id=case_id, reason=str(e))
        async for session in get_db_session():
            repo = RecoveryCaseRepository(session)
            case = await repo.get(case_id)
            case.state = state_machine.transition(case.state, CaseState.ESCALATED)
            await repo.update(case.id, case)
            break
    except IdempotencyConflictError:
        logger.info("Saga idempotency conflict, skipping execution", case_id=case_id)
    except Exception as e:
        logger.error("Saga step failed: handle_action_proposed", case_id=case_id, error=str(e))
        async for session in get_db_session():
            repo = RecoveryCaseRepository(session)
            case = await repo.get(case_id)
            case.state = state_machine.transition(case.state, CaseState.FAILED)
            await repo.update(case.id, case)
            break

async def handle_action_executed(payload: Dict[str, Any]):
    """Handles the event after action execution to close the case."""
    case_id = payload.get("case_id")
    if not case_id:
        return
        
    logger.info("Saga: processing action executed", case_id=case_id)
    try:
        async for session in get_db_session():
            repo = RecoveryCaseRepository(session)
            case = await repo.get(case_id)
            
            case.state = state_machine.transition(case.state, CaseState.VERIFICATION)
            case.state = state_machine.transition(case.state, CaseState.RECOVERED)
            case.state = state_machine.transition(case.state, CaseState.CLOSED)
            await repo.update(case.id, case)
            
            logger.info("Saga: case successfully closed", case_id=case_id)
            break
    except Exception as e:
        logger.error("Saga step failed: handle_action_executed", case_id=case_id, error=str(e))

def setup_saga_subscribers():
    logger.info("Setting up Saga event subscribers...")
    event_bus.subscribe("recovery.case.created", handle_case_created)
    event_bus.subscribe("recovery.action.proposed", handle_action_proposed)
    event_bus.subscribe("recovery.action.executed", handle_action_executed)
