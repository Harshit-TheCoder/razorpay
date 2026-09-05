import asyncio
import uuid
from datetime import datetime, timedelta
import random

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.session import get_db_session
from app.recovery.models import RecoveryCase, RecoveryAttempt
from app.payments.models import Payment
from app.subscriptions.models import Subscription
from app.checkout.models import CheckoutRecord
from app.core.db.postgres.base_models import Merchant, Customer
from app.core.logging_db.mongo_client import get_mongo_db

async def seed_data():
    session_generator = get_db_session()
    session: AsyncSession = await anext(session_generator)
    
    try:
        # Create a mock merchant
        merchant_id = "demo_merchant"
        merchant = Merchant(
            id=merchant_id,
            name="Demo Merchant Inc.",
            razorpay_key_ref="rzp_test_12345",
            policy_profile_id="policy_1"
        )
        session.add(merchant)
        
        customer_id = "demo_customer"
        customer = Customer(
            id=customer_id,
            merchant_id=merchant_id,
            razorpay_customer_id="cust_rzp_123",
            contact_prefs="email"
        )
        session.add(customer)
        
        # Create mock cases and source references
        scenario_types = ["failed_payment", "checkout_abandonment", "subscription_recovery"]
        states = ["DETECTED", "ENGAGED", "RECOVERED", "FAILED", "ESCALATED"]
        
        now = datetime.now()
        for i in range(20):
            scenario = random.choice(scenario_types)
            source_ref_id = f"src_{uuid.uuid4().hex[:8]}"
            
            # Generate the source reference entity
            if scenario == "failed_payment":
                real_errors = ["INSUFFICIENT_FUNDS", "PAYMENT_DECLINED", "GATEWAY_ERROR", "INVALID_CARD", "NETWORK_TIMEOUT"]
                real_reasons = [
                    "Payment failed due to insufficient funds",
                    "Issuing bank declined the transaction",
                    "Upstream gateway returned 502",
                    "Invalid card details provided",
                    "Bank timeout during 3D secure authentication"
                ]
                err_idx = random.randint(0, len(real_errors) - 1)
                
                payment = Payment(
                    id=source_ref_id,
                    merchant_id=merchant_id,
                    order_id=f"order_{random.randint(100, 999)}",
                    razorpay_payment_id=f"pay_{uuid.uuid4().hex[:10]}",
                    status="failed",
                    error_code=real_errors[err_idx],
                    error_reason=real_reasons[err_idx],
                    error_source="customer" if "FUNDS" in real_errors[err_idx] or "CARD" in real_errors[err_idx] else "gateway"
                )
                session.add(payment)
            elif scenario == "subscription_recovery":
                sub = Subscription(
                    id=source_ref_id,
                    merchant_id=merchant_id,
                    customer_id=customer_id,
                    razorpay_subscription_id=f"sub_{uuid.uuid4().hex[:10]}",
                    type="recurring",
                    status="halted"
                )
                session.add(sub)
            elif scenario == "checkout_abandonment":
                checkout = CheckoutRecord(
                    id=source_ref_id,
                    merchant_id=merchant_id,
                    customer_id=customer_id,
                    cart_snapshot={"items": [{"id": "item_1", "price": random.randint(500, 15000), "qty": 1}], "currency": "INR"},
                    status="abandoned"
                )
                session.add(checkout)
            
            state = random.choice(states)
            closed = None
            if state in ["RECOVERED", "FAILED"]:
                closed = now - timedelta(hours=random.randint(1, 24))
            
            case_id = f"case_{1000 + i}"
            case = RecoveryCase(
                id=case_id,
                merchant_id=merchant_id,
                scenario_type=scenario,
                source_ref=source_ref_id,
                amount=random.randint(50000, 1500000), # 500 to 15,000 INR
                state=state,
                opened_at=now - timedelta(days=random.randint(1, 5)),
                closed_at=closed
            )
            session.add(case)
            
            # Generate Recovery Attempts for the case
            attempt_count = random.randint(1, 4)
            for j in range(attempt_count):
                attempt_state = "COMPLETED" if j < attempt_count - 1 else ("PENDING" if state == "ENGAGED" else "FAILED")
                if state == "RECOVERED" and j == attempt_count - 1:
                    attempt_state = "COMPLETED"
                    
                attempt = RecoveryAttempt(
                    id=f"att_{uuid.uuid4().hex[:8]}",
                    case_id=case_id,
                    attempt_number=j + 1,
                    action_type="SEND_EMAIL" if j == 0 else "SEND_SMS",
                    status=attempt_state,
                    executed_at=now - timedelta(days=random.randint(1, 5)) + timedelta(hours=j*12),
                    result={"delivery_status": "delivered", "opened": True} if attempt_state == "COMPLETED" else None
                )
                session.add(attempt)
                
            # Seed MongoDB Audit Logs for this case
            db = get_mongo_db()
            audit_collection = db["audit_logs"]
            
            # Create a detected log
            await audit_collection.insert_one({
                "action": "CASE_CREATED",
                "actor": "system",
                "case_id": case_id,
                "merchant_id": merchant_id,
                "previous_state": None,
                "new_state": "DETECTED",
                "payload": {"reason": scenario},
                "timestamp": now - timedelta(days=5)
            })
            
            # Create a final state log
            await audit_collection.insert_one({
                "action": "STATE_TRANSITION",
                "actor": "agent_llm",
                "case_id": case_id,
                "merchant_id": merchant_id,
                "previous_state": "DETECTED",
                "new_state": state,
                "payload": {"rationale": "Policy engine approved transition."},
                "timestamp": now - timedelta(days=2)
            })

        
        await session.commit()
        print("Successfully seeded 1 merchant and 20 cases.")
    except Exception as e:
        print(f"Error seeding data: {e}")
        await session.rollback()
    finally:
        await session.close()

if __name__ == "__main__":
    asyncio.run(seed_data())
