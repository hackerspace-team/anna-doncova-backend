from datetime import datetime, timezone

from app.firebase import db
from app.models.enrollment import TariffType, PaymentMethod, PaymentType, PaymentStatus


async def write_enrollment(
    id: str,
    name: str,
    phone: str,
    email: str,
    telegram: str,
    activity: str,
    tariff: TariffType,
    amount: float,
    income_amount: float,
    payment_id: str,
    payment_method: PaymentMethod,
    payment_type: PaymentType,
    payment_status: PaymentStatus,
):
    enrollment_ref = db.collection('enrollments').document(id)

    current_time = datetime.now(timezone.utc)
    await enrollment_ref.set({
        'id': id,
        'name': name,
        'phone': phone,
        'email': email,
        'telegram': telegram,
        'activity': activity,
        'tariff': tariff,
        'amount': amount,
        'income_amount': income_amount,
        'payment_id': payment_id,
        'payment_method': payment_method,
        'payment_type': payment_type,
        'payment_status': payment_status,
        'created_date': current_time,
        'edited_date': current_time,
    })
