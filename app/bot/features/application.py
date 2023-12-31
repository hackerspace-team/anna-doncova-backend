from typing import List, Optional
from datetime import datetime, timezone

from app.firebase import db
from app.models.application import Application


async def write_application(name: str, phone: str, email: str, activities: List[str], type: str):
    await db.collection('applications').document().set({
        'name': name,
        'phone': phone,
        'email': email,
        'activities': activities,
        'type': type,
        'created_date': datetime.now(timezone.utc),
    })


async def get_applications(start_date: Optional[datetime] = None,
                           end_date: Optional[datetime] = None) -> List[Application]:
    applications_query = db.collection("applications")

    if start_date:
        applications_query = applications_query.where("created_date", ">=", start_date)
    if end_date:
        applications_query = applications_query.where("created_date", "<=", end_date)

    applications = applications_query.stream()
    return [Application(**application.to_dict()) async for application in applications]
