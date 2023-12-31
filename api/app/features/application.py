from typing import List
from datetime import datetime, timezone

from app.firebase import db


async def write_application(name: str, phone: str, email: str, activities: List[str], type: str):
    application_ref = db.collection('applications').document()
    await application_ref.set({
        'id': application_ref.id,
        'name': name,
        'phone': phone,
        'email': email,
        'activities': activities,
        'type': type,
        'created_date': datetime.now(timezone.utc),
    })
