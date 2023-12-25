from datetime import datetime, timezone

from app.models.common import Currency
from app.models.subscription import SubscriptionType
from app.models.user import UserQuota


class TransactionType:
    INCOME = 'INCOME'
    EXPENSE = 'EXPENSE'


class ServiceType(SubscriptionType, UserQuota):
    OTHER = "OTHER"


class Transaction:
    id: str
    user_id: str
    type: TransactionType
    service: ServiceType
    amount: float
    currency: Currency
    quantity: int
    created_at: datetime
    edited_at: datetime

    def __init__(self,
                 id: str,
                 user_id: str,
                 type: TransactionType,
                 service: ServiceType,
                 amount: float,
                 currency: Currency,
                 quantity=1,
                 created_at=None,
                 edited_at=None):
        self.id = str(id)
        self.user_id = str(user_id)
        self.type = type
        self.service = service.upper()
        self.amount = amount
        self.currency = currency
        self.quantity = quantity

        current_time = datetime.now(timezone.utc)
        self.created_at = created_at if created_at is not None else current_time
        self.edited_at = edited_at if edited_at is not None else current_time

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'service': self.service,
            'amount': self.amount,
            'currency': self.currency,
            'quantity': self.quantity,
            'created_at': self.created_at,
            'edited_at': self.edited_at
        }
