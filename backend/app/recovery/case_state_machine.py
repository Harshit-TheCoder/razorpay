from app.exceptions.domain_exceptions import InvalidCaseStateTransitionError

class CaseState:
    DETECTED = "DETECTED"
    INVESTIGATING = "INVESTIGATING"
    DIAGNOSED = "DIAGNOSED"
    ACTION_PROPOSED = "ACTION_PROPOSED"
    POLICY_CHECK = "POLICY_CHECK"
    ACTION_EXECUTED = "ACTION_EXECUTED"
    VERIFICATION = "VERIFICATION"
    RECOVERED = "RECOVERED"
    FAILED = "FAILED"
    ESCALATED = "ESCALATED"
    CLOSED = "CLOSED"

    VALID_TRANSITIONS = {
        DETECTED: [INVESTIGATING, ESCALATED],
        INVESTIGATING: [DIAGNOSED, FAILED, ESCALATED],
        DIAGNOSED: [ACTION_PROPOSED, ESCALATED],
        ACTION_PROPOSED: [POLICY_CHECK],
        POLICY_CHECK: [ACTION_EXECUTED, ESCALATED], # Blocks go to ESCALATED
        ACTION_EXECUTED: [VERIFICATION, FAILED],
        VERIFICATION: [RECOVERED, FAILED, ESCALATED],
        RECOVERED: [CLOSED],
        FAILED: [ACTION_PROPOSED, CLOSED], # Retry loops back to proposed or closes
        ESCALATED: [CLOSED] # Human intervention
    }

class CaseStateMachine:
    @staticmethod
    def transition(current_state: str, next_state: str) -> str:
        allowed = CaseState.VALID_TRANSITIONS.get(current_state, [])
        if next_state not in allowed:
            raise InvalidCaseStateTransitionError(current_state, next_state)
        return next_state
