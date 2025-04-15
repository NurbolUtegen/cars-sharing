import logging

logger = logging.getLogger(__name__)

class PaymentService:
    def process_payment(self, user_id, amount):
        logger.info(f"Processing payment of ${amount} for user {user_id}")
        return {"status": "success", "transaction_id": "123456"}