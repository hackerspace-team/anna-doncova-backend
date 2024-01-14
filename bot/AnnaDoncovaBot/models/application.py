from datetime import datetime, timezone
from typing import List


class Application:
    id: str
    name: str
    phone: str
    email: str
    telegram: str
    activities: List[str]
    created_date: datetime

    def __init__(self,
                 id: str,
                 name: str,
                 phone: str,
                 email: str,
                 telegram: str,
                 activities: List[str],
                 created_date=None):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.telegram = telegram
        self.activities = activities

        current_time = datetime.now(timezone.utc)
        self.created_date = created_date if created_date is not None else current_time

    def to_dict(self):
        return vars(self)
