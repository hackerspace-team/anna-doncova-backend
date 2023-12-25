import re
from datetime import datetime, timedelta, timezone

from app.models.common import Currency


class SubscriptionType:
    FREE = 'FREE'
    STANDARD = 'STANDARD'
    VIP = 'VIP'
    PLATINUM = 'PLATINUM'


class SubscriptionPeriod:
    MONTH1 = 'MONTH_1'
    MONTHS3 = 'MONTHS_3'
    MONTHS6 = 'MONTHS_6'


class SubscriptionStatus:
    ACTIVE = 'ACTIVE'
    WAITING = 'WAITING'
    FINISHED = 'FINISHED'
    ERROR = 'ERROR'


class Subscription:
    id: str
    user_id: str
    type: SubscriptionType
    period: SubscriptionPeriod
    status: SubscriptionStatus
    currency: Currency
    amount: float
    provider_payment_charge_id: str
    start_date: datetime
    end_date: datetime
    created_at: datetime
    edited_at: datetime

    def __init__(self,
                 id: str,
                 user_id: str,
                 type: SubscriptionType,
                 period: SubscriptionPeriod,
                 status: SubscriptionStatus,
                 currency: Currency,
                 amount: float,
                 provider_payment_charge_id="",
                 start_date=None,
                 end_date=None,
                 created_at=None,
                 edited_at=None):
        self.id = str(id)
        self.user_id = str(user_id)
        self.type = type
        self.period = period
        self.status = status
        self.currency = currency
        self.amount = amount
        self.provider_payment_charge_id = provider_payment_charge_id

        self.start_date = start_date if start_date is not None else datetime.now(timezone.utc)
        if period == SubscriptionPeriod.MONTH1:
            self.end_date = self.start_date + timedelta(days=30)
        elif period == SubscriptionPeriod.MONTHS3:
            self.end_date = self.start_date + timedelta(days=90)
        elif period == SubscriptionPeriod.MONTHS6:
            self.end_date = self.start_date + timedelta(days=180)
        else:
            self.end_date = end_date

        current_time = datetime.now(timezone.utc)
        self.created_at = created_at if created_at is not None else current_time
        self.edited_at = edited_at if edited_at is not None else current_time

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'period': self.period,
            'status': self.status,
            'currency': self.currency,
            'amount': self.amount,
            'provider_payment_charge_id': self.provider_payment_charge_id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'created_at': self.created_at,
            'edited_at': self.edited_at
        }

    @staticmethod
    def get_prices(currency: Currency):
        prices = {
            SubscriptionType.STANDARD: '',
            SubscriptionType.VIP: '',
            SubscriptionType.PLATINUM: ''
        }

        if currency == Currency.RUB:
            prices[SubscriptionType.STANDARD] = '299₽'
            prices[SubscriptionType.VIP] = '999₽'
            prices[SubscriptionType.PLATINUM] = '1 999₽'
        elif currency == Currency.EUR:
            prices[SubscriptionType.STANDARD] = '2.99€'
            prices[SubscriptionType.VIP] = '9.99€'
            prices[SubscriptionType.PLATINUM] = '19.99€'
        else:
            prices[SubscriptionType.STANDARD] = '$2.99'
            prices[SubscriptionType.VIP] = '$9.99'
            prices[SubscriptionType.PLATINUM] = '$19.99'

        return prices

    @staticmethod
    def get_emojis():
        return {
            SubscriptionType.FREE: '',
            SubscriptionType.STANDARD: '⭐',
            SubscriptionType.VIP: '🔥',
            SubscriptionType.PLATINUM: '💎'
        }

    @staticmethod
    def get_price(currency: Currency, subscription_type: SubscriptionType, subscription_period: SubscriptionPeriod):
        price_discount = {
            SubscriptionPeriod.MONTH1: 0,
            SubscriptionPeriod.MONTHS3: 5,
            SubscriptionPeriod.MONTHS6: 10
        }
        price_period = {
            SubscriptionPeriod.MONTH1: 1,
            SubscriptionPeriod.MONTHS3: 3,
            SubscriptionPeriod.MONTHS6: 6,
        }
        prices = Subscription.get_prices(currency)
        price_raw = prices[subscription_type]
        price_clear = re.sub(r'[^\d.]', '', price_raw)
        price = float(price_clear) if '.' in price_clear else int(price_clear)
        price_with_period = price * price_period[subscription_period]
        price_with_discount = price_with_period - (price_with_period * (price_discount[subscription_period] / 100.0))

        return int(price_with_discount)
