import json
import logging
import uuid

import aiohttp
from aiohttp import BasicAuth
from telegram import Bot
from yookassa import Configuration

from AnnaDoncovaBackend.settings import TELEGRAM_TOKEN, ADMIN_CHAT_IDS
from app.models.enrollment import TariffType


async def send_message_to_admins(message: str, parse_mode='HTML'):
    bot = Bot(token=TELEGRAM_TOKEN)

    for chat_id in ADMIN_CHAT_IDS:
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode=parse_mode,
            )
        except Exception as error:
            logging.error(error)


async def create_payment(amount: float, email: str, name: str, tariff: TariffType) -> dict:
    url = "https://api.yookassa.ru/v3/payments"
    headers = {
        "Content-Type": "application/json",
        "Idempotence-Key": str(uuid.uuid4()),
    }
    payload = {
        "amount": {
            "value": amount,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://annadoncova.com"
        },
        "capture": True,
        "description": f'Оплата курса "Нейросети в жизни и бизнесе".\n'
                       f'Тариф "{tariff}".\n'
                       f'Почта клиента: {email}.',
        "receipt": {
            "customer": {
                "full_name": name,
                "email": email,
            },
            "items": [
                {
                    "amount": {
                        "value": amount,
                        "currency": "RUB"
                    },
                    "description": f'Оплата курса "Нейросети в жизни и бизнесе".\n'
                                   f'Тариф "{tariff}".\n'
                                   f'Почта клиента: {email}.',
                    "vat_code": 1,
                    "quantity": 1,
                }
            ]
        }
    }

    async with aiohttp.ClientSession(auth=BasicAuth(Configuration.account_id, Configuration.secret_key)) as session:
        async with session.post(url, headers=headers, data=json.dumps(payload)) as response:
            if response.ok:
                body = await response.json()
                return body
