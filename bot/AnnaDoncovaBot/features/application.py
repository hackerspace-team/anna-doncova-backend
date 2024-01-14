from typing import List, Optional
from datetime import datetime

from google.cloud.firestore import Query

from AnnaDoncovaBot.firebase import db
from AnnaDoncovaBot.models.application import Application


async def get_applications(start_date: Optional[datetime] = None,
                           end_date: Optional[datetime] = None) -> List[Application]:
    applications_query = db.collection("applications")

    if start_date:
        applications_query = applications_query.where("created_date", ">=", start_date)
    if end_date:
        applications_query = applications_query.where("created_date", "<=", end_date)

    applications = applications_query.order_by("created_date", direction=Query.ASCENDING).stream()
    return [
        Application(
            id=application.to_dict().get('id', None),
            name=application.to_dict().get('name', None),
            phone=application.to_dict().get('phone', None),
            email=application.to_dict().get('email', None),
            telegram=application.to_dict().get('telegram', None),
            activities=application.to_dict().get('activities', None),
            created_date=application.to_dict().get('created_date', None)
        ) async for application in applications
    ]
