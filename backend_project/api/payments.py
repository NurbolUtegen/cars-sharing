from fastapi import APIRouter
from pydantic import BaseModel
from payments.payment_service import PaymentService

router = APIRouter()
payment_service = PaymentService()

class PaymentRequest(BaseModel):
    user_id: int
    amount: float

@router.post("/pay")
def pay(req: PaymentRequest):
    result = payment_service.process_payment(req.user_id, req.amount)
    return result