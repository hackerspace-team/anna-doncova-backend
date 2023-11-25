from enum import Enum
from datetime import datetime

from app.bot.constants import GPT3_DAILY_LIMIT_MESSAGES


class Model(Enum):
    GPT3 = 'gpt-3.5-turbo'


class User:
    id: str
    first_name: str
    last_name: str
    username: str
    current_chat_id: str
    telegram_chat_id: str
    language_code: str
    is_premium: bool
    current_model: str
    daily_limits: dict

    DEFAULT_DAILY_LIMITS = {
        "GPT3": GPT3_DAILY_LIMIT_MESSAGES
    }

    def __init__(self,
                 id,
                 first_name,
                 last_name,
                 username,
                 current_chat_id,
                 telegram_chat_id,
                 language_code="en",
                 is_premium=False,
                 current_model=Model.GPT3.value,
                 daily_limits=None,
                 created_at=datetime.now(),
                 edited_at=datetime.now()):
        self.id = str(id)
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.language_code = language_code
        self.is_premium = is_premium
        self.current_model = current_model
        self.current_chat_id = str(current_chat_id)
        self.telegram_chat_id = str(telegram_chat_id)
        self.daily_limits = daily_limits if daily_limits is not None else self.DEFAULT_DAILY_LIMITS
        self.created_at = created_at
        self.edited_at = edited_at

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'language_code': self.language_code,
            'is_premium': self.is_premium,
            'current_model': self.current_model,
            'current_chat_id': self.current_chat_id,
            'telegram_chat_id': self.telegram_chat_id,
            'daily_limits': self.daily_limits,
            'created_at': self.created_at,
            'edited_at': self.edited_at
        }


class Chat:
    id: str
    telegram_chat_id: str
    title: str

    def __init__(self, id, telegram_chat_id, title="New chat", created_at=datetime.now(), edited_at=datetime.now()):
        self.id = str(id)
        self.telegram_chat_id = str(telegram_chat_id)
        self.title = title
        self.created_at = created_at
        self.edited_at = edited_at

    def to_dict(self):
        return {
            'id': self.id,
            'telegram_chat_id': self.telegram_chat_id,
            'title': self.title,
            'created_at': self.created_at,
            'edited_at': self.edited_at
        }


class Message:
    id: str
    chat_id: str
    sender: str
    sender_id: str
    content: str

    def __init__(self, id, chat_id, sender, sender_id, content, created_at=datetime.now(), edited_at=datetime.now()):
        self.id = str(id)
        self.chat_id = str(chat_id)
        self.sender = sender
        self.sender_id = str(sender_id)
        self.content = content
        self.created_at = created_at
        self.edited_at = edited_at

    def to_dict(self):
        return {
            'id': self.id,
            'chat_id': self.chat_id,
            'sender': self.sender,
            'sender_id': self.sender_id,
            'content': self.content,
            'created_at': self.created_at,
            'edited_at': self.edited_at
        }
