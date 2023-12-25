from datetime import datetime, timezone
from typing import List


class Chat:
    id: str
    user_id: str
    telegram_chat_ids: List[str]
    title: str
    role: str
    created_at: datetime
    edited_at: datetime

    def __init__(self,
                 id: str,
                 user_id: str,
                 telegram_chat_ids: List[str],
                 title="New chat",
                 role=None,
                 created_at=None,
                 edited_at=None):
        self.id = str(id)
        self.user_id = user_id
        self.telegram_chat_ids = [str(telegram_chat_id) for telegram_chat_id in telegram_chat_ids]
        self.title = title
        self.role = role if role is not None else "PERSONAL_ASSISTANT"

        current_time = datetime.now(timezone.utc)
        self.created_at = created_at if created_at is not None else current_time
        self.edited_at = edited_at if edited_at is not None else current_time

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'telegram_chat_ids': self.telegram_chat_ids,
            'title': self.title,
            'role': self.role,
            'created_at': self.created_at,
            'edited_at': self.edited_at
        }
