from typing import Optional, Dict

from app.firebase import db
from app.models.common import Currency
from app.models.transaction import Transaction, TransactionType, ServiceType


async def get_transaction(transaction_id: str) -> Optional[Transaction]:
    transaction_ref = db.collection("transactions").document(str(transaction_id))
    transaction = await transaction_ref.get()

    if transaction.exists:
        return Transaction(**transaction.to_dict())


async def create_transaction_object(user_id: str,
                                    type: TransactionType,
                                    service: ServiceType,
                                    amount: float,
                                    currency: Currency,
                                    quantity=1) -> Transaction:
    transaction_ref = db.collection('transactions').document()
    return Transaction(
        id=transaction_ref.id,
        user_id=user_id,
        type=type,
        service=service,
        amount=amount,
        currency=currency,
        quantity=quantity,
    )


async def write_transaction(user_id: str,
                            type: TransactionType,
                            service: ServiceType,
                            amount: float,
                            currency: Currency,
                            quantity=1) -> Transaction:
    transaction = await create_transaction_object(user_id, type, service, amount, currency, quantity)
    await db.collection('transactions').document(transaction.id).set(transaction.to_dict())

    return transaction


async def write_transaction_in_transaction(transaction,
                                           user_id: str,
                                           type: TransactionType,
                                           service: ServiceType,
                                           amount: float,
                                           currency: Currency,
                                           quantity=1) -> Transaction:
    transaction_object = await create_transaction_object(user_id, type, service, amount, currency, quantity)
    transaction.set(db.collection('transactions').document(transaction_object.id), transaction_object.to_dict())

    return transaction_object


async def update_transaction(transaction_id: str, data: Dict):
    transaction_ref = db.collection('transactions').document(transaction_id)
    await transaction_ref.update(data)
