# Registry of notification templates
# In a real app, this would likely live in the DB or an external service (like SendGrid dynamic templates)

TEMPLATES = {
    "payment_failed_v1": {
        "subject": "Action Required: Your recent payment failed",
        "body": "Hi {name},\n\nWe couldn't process your payment of {amount}. Please update your payment method to avoid service interruption.\n\nThanks,\n{merchant_name}"
    },
    "offer_discount_v1": {
        "subject": "Special Offer Just For You!",
        "body": "Hi {name},\n\nWe noticed you had some trouble with your checkout. Here is a {discount}% off coupon to complete your purchase: {coupon_code}\n\nThanks,\n{merchant_name}"
    }
}
