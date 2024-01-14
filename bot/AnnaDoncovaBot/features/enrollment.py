from typing import List, Optional
from datetime import datetime, timezone

from google.cloud.firestore import Query

from AnnaDoncovaBot.firebase import db
from AnnaDoncovaBot.models.enrollment import Enrollment


async def get_enrollment(enrollment_id: str) -> Enrollment:
    enrollment_ref = db.collection("enrollments").document(enrollment_id)
    enrollment = await enrollment_ref.get()

    if enrollment.exists:
        enrollment_dict = enrollment.to_dict()
        return Enrollment(
            id=enrollment_dict.get('id', None),
            name=enrollment_dict.get('name', None),
            phone=enrollment_dict.get('phone', None),
            email=enrollment_dict.get('email', None),
            telegram=enrollment_dict.get('telegram', None),
            activity=enrollment_dict.get('activity', None),
            tariff=enrollment_dict.get('tariff', None),
            amount=enrollment_dict.get('amount', None),
            income_amount=enrollment_dict.get('income_amount', None),
            payment_id=enrollment_dict.get('payment_id', None),
            payment_method=enrollment_dict.get('payment_method', None),
            payment_type=enrollment_dict.get('payment_type', None),
            payment_status=enrollment_dict.get('payment_status', None),
            created_date=enrollment_dict.get('created_date', None),
            edited_date=enrollment_dict.get('edited_date', None),
        )


async def get_enrollment_by_payment_id(payment_id: str) -> Enrollment:
    enrollment_stream = db.collection("enrollments").where("payment_id", "==", payment_id).limit(1).stream()

    async for doc in enrollment_stream:
        enrollment_dict = doc.to_dict()
        return Enrollment(
            id=enrollment_dict.get('id', None),
            name=enrollment_dict.get('name', None),
            phone=enrollment_dict.get('phone', None),
            email=enrollment_dict.get('email', None),
            telegram=enrollment_dict.get('telegram', None),
            activity=enrollment_dict.get('activity', None),
            tariff=enrollment_dict.get('tariff', None),
            amount=enrollment_dict.get('amount', None),
            income_amount=enrollment_dict.get('income_amount', None),
            payment_id=enrollment_dict.get('payment_id', None),
            payment_method=enrollment_dict.get('payment_method', None),
            payment_type=enrollment_dict.get('payment_type', None),
            payment_status=enrollment_dict.get('payment_status', None),
            created_date=enrollment_dict.get('created_date', None),
            edited_date=enrollment_dict.get('edited_date', None),
        )


async def get_enrollments(start_date: Optional[datetime] = None,
                          end_date: Optional[datetime] = None) -> List[Enrollment]:
    enrollments_query = db.collection("enrollments")

    if start_date:
        enrollments_query = enrollments_query.where("created_date", ">=", start_date)
    if end_date:
        enrollments_query = enrollments_query.where("created_date", "<=", end_date)

    enrollments = enrollments_query.order_by("created_date", direction=Query.DESCENDING).stream()
    return [
        Enrollment(
            id=enrollment.to_dict().get('id', None),
            name=enrollment.to_dict().get('name', None),
            phone=enrollment.to_dict().get('phone', None),
            email=enrollment.to_dict().get('email', None),
            telegram=enrollment.to_dict().get('telegram', None),
            activity=enrollment.to_dict().get('activity', None),
            tariff=enrollment.to_dict().get('tariff', None),
            amount=enrollment.to_dict().get('amount', None),
            income_amount=enrollment.to_dict().get('income_amount', None),
            payment_id=enrollment.to_dict().get('payment_id', None),
            payment_method=enrollment.to_dict().get('payment_method', None),
            payment_type=enrollment.to_dict().get('payment_type', None),
            payment_status=enrollment.to_dict().get('payment_status', None),
            created_date=enrollment.to_dict().get('created_date', None),
            edited_date=enrollment.to_dict().get('edited_date', None),
        ) async for enrollment in enrollments
    ]


async def update_enrollment(enrollment_id: str, data: dict):
    enrollment_ref = db.collection('enrollments').document(enrollment_id)
    data['edited_at'] = datetime.now(timezone.utc)

    await enrollment_ref.update(data)
