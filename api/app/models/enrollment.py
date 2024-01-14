from datetime import datetime, timezone


class TariffType:
    STANDARD = 'STANDARD'
    VIP = 'VIP'
    PLATINUM = 'PLATINUM'


class PaymentMethod:
    YOOKASSA = 'YOOKASSA'
    PAYPAL = 'PAYPAL'


class PaymentType:
    PREPAYMENT = 'PREPAYMENT'
    FULL_PAYMENT = 'FULL_PAYMENT'


class PaymentStatus:
    PENDING = 'PENDING'
    CANCELED = 'CANCELED'
    SUCCEEDED = 'SUCCEEDED'


class Enrollment:
    id: str
    name: str
    phone: str
    email: str
    telegram: str
    activity: str
    tariff: TariffType
    amount: float
    income_amount: float
    payment_id: str
    payment_method: PaymentMethod
    payment_type: PaymentType
    payment_status: PaymentStatus
    created_date: datetime
    edited_date: datetime

    def __init__(self,
                 id: str,
                 name: str,
                 phone: str,
                 email: str,
                 telegram: str,
                 activity: str,
                 tariff: TariffType,
                 amount: float,
                 income_amount: float,
                 payment_id: str,
                 payment_method: PaymentMethod,
                 payment_type: PaymentType,
                 payment_status: PaymentStatus,
                 created_date=None,
                 edited_date=None):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.telegram = telegram
        self.activity = activity
        self.tariff = tariff
        self.amount = amount
        self.income_amount = income_amount
        self.payment_id = payment_id
        self.payment_method = payment_method
        self.payment_type = payment_type
        self.payment_status = payment_status

        current_time = datetime.now(timezone.utc)
        self.created_date = created_date if created_date is not None else current_time
        self.edited_date = edited_date if edited_date is not None else current_time

    def to_dict(self):
        return vars(self)
