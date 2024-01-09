from datetime import datetime, timezone
from typing import List


class ApplicationType:
    PRE_REGISTER = 'PRE_REGISTER'
    REGISTER = 'REGISTER'


class Application:
    id: str
    name: str
    phone: str
    email: str
    telegram: str
    activities: List[str]
    type: ApplicationType
    created_date: datetime

    def __init__(self,
                 id: str,
                 name: str,
                 phone: str,
                 email: str,
                 telegram: str,
                 activities: List[str],
                 type: ApplicationType,
                 created_date=None):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.telegram = telegram
        self.activities = activities
        self.type = type

        current_time = datetime.now(timezone.utc)
        self.created_date = created_date if created_date is not None else current_time

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'telegram': self.telegram,
            'activities': self.activities,
            'type': self.type,
            'created_date': self.created_date,
        }
