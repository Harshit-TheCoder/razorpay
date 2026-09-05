from app.customer.repository import CustomerRepository
from app.customer.schemas import CustomerProfileDTO, CustomerHistoryDTO

class CustomerService:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository
        
    async def get_customer_profile(self, customer_id: str) -> CustomerProfileDTO:
        cust = await self.repository.get_customer(customer_id)
        if not cust:
            # For simplicity, returning a dummy profile rather than raising if missing
            return CustomerProfileDTO(
                customer_id=customer_id, merchant_id="", 
                history=CustomerHistoryDTO(customer_id=customer_id, total_orders=0, total_payments=0, successful_payments=0, failed_payments=0, active_subscriptions=0)
            )
            
        orders = await self.repository.count_customer_orders(customer_id)
        payment_stats = await self.repository.get_customer_payment_stats(customer_id)
        
        history = CustomerHistoryDTO(
            customer_id=customer_id,
            total_orders=orders,
            total_payments=payment_stats["total"],
            successful_payments=payment_stats["successful"],
            failed_payments=payment_stats["failed"],
            active_subscriptions=0 # Stubbed
        )
        
        return CustomerProfileDTO(
            customer_id=customer_id,
            merchant_id=cust.merchant_id,
            history=history
        )
