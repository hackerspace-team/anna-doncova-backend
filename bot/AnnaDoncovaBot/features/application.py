from typing import List, Optional
from datetime import datetime

from AnnaDoncovaBot.firebase import db
from AnnaDoncovaBot.models.application import Application


async def get_applications(start_date: Optional[datetime] = None,
                           end_date: Optional[datetime] = None) -> List[Application]:
    applications_query = db.collection("applications")

    if start_date:
        applications_query = applications_query.where("created_date", ">=", start_date)
    if end_date:
        applications_query = applications_query.where("created_date", "<=", end_date)

    applications = applications_query.stream()
    return [Application(**application.to_dict()) async for application in applications]
