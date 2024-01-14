from typing import List
from datetime import datetime, timezone

from app.firebase import db


async def write_application(id: str, name: str, phone: str, email: str, telegram: str, activities: List[str]):
    application_ref = db.collection('applications').document(id)
    await application_ref.set({
        'id': application_ref.id,
        'name': name,
        'phone': phone,
        'email': email,
        'telegram': telegram,
        'activities': activities,
        'created_date': datetime.now(timezone.utc),
    })
