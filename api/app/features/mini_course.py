from datetime import datetime, timezone

from app.firebase import db
from app.models.enrollment import PaymentMethod, PaymentStatus


async def write_mini_course(
    id: str,
    name: str,
    email: str,
    telegram: str,
    amount: float,
    income_amount: float,
    payment_id: str,
    payment_method: PaymentMethod,
    payment_status: PaymentStatus,
):
    mini_course_ref = db.collection('mini_courses').document(id)

    current_time = datetime.now(timezone.utc)
    await mini_course_ref.set({
        'id': id,
        'name': name,
        'email': email,
        'telegram': telegram,
        'amount': amount,
        'income_amount': income_amount,
        'payment_id': payment_id,
        'payment_method': payment_method,
        'payment_status': payment_status,
        'created_date': current_time,
        'edited_date': current_time,
    })
