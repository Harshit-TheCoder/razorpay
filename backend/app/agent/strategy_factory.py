from app.agent.strategies.base import RecoveryStrategy
from app.agent.strategies.failed_payment import FailedPaymentStrategy
from app.agent.strategies.checkout_abandonment import CheckoutAbandonmentStrategy
from app.agent.strategies.subscription_recovery import SubscriptionRecoveryStrategy

from app.agent.strategies.premium_recovery import PremiumRecoveryStrategy
from app.agent.strategies.revenue_drop import RevenueDropStrategy
from app.agent.strategies.churn_recovery import ChurnRecoveryStrategy
from app.agent.strategies.volume_drop import VolumeDropStrategy

class StrategyFactory:
    _strategies = {
        "failed_payment": FailedPaymentStrategy(),
        "checkout_abandonment": CheckoutAbandonmentStrategy(),
        "subscription_recovery": SubscriptionRecoveryStrategy(),
        "premium_recovery": PremiumRecoveryStrategy(),
        "revenue_drop": RevenueDropStrategy(),
        "churn_recovery": ChurnRecoveryStrategy(),
        "volume_drop": VolumeDropStrategy()
    }

    @classmethod
    def get(cls, scenario_type: str) -> RecoveryStrategy:
        strategy = cls._strategies.get(scenario_type)
        if not strategy:
            # Fallback to failed payment strategy if unknown, or raise an error.
            # We'll use failed_payment as a generic fallback for the hackathon.
            return cls._strategies["failed_payment"]
        return strategy
