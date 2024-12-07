from datetime import datetime, timezone

from app.models.enrollment import PaymentMethod, PaymentStatus


class MiniCourse:
    id: str
    name: str
    email: str
    telegram: str
    amount: float
    income_amount: float
    payment_id: str
    payment_method: PaymentMethod
    payment_status: PaymentStatus
    created_date: datetime
    edited_date: datetime

    def __init__(self,
                 id: str,
                 name: str,
                 email: str,
                 telegram: str,
                 amount: float,
                 income_amount: float,
                 payment_id: str,
                 payment_method: PaymentMethod,
                 payment_status: PaymentStatus,
                 created_date=None,
                 edited_date=None):
        self.id = id
        self.name = name
        self.email = email
        self.telegram = telegram
        self.amount = amount
        self.income_amount = income_amount
        self.payment_id = payment_id
        self.payment_method = payment_method
        self.payment_status = payment_status

        current_time = datetime.now(timezone.utc)
        self.created_date = created_date if created_date is not None else current_time
        self.edited_date = edited_date if edited_date is not None else current_time

    def to_dict(self):
        return vars(self)
