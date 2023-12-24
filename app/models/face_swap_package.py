from datetime import datetime
from typing import List

from app.models.user import UserGender


class FaceSwapPackageName:
    CELEBRITIES = {
        "name": "CELEBRITIES",
        f"{UserGender.MALE}_files": [
            '1_ElonMusk.jpeg',
            '2_LeonardoDiCaprio.jpg'
        ],
        f"{UserGender.FEMALE}_files": [
            '1_Beyonce.jpeg',
            '2_EmmaWatson.jpeg'
        ]
    }


class FaceSwapPackage:
    id: str
    user_id: str
    name: str
    used_images: List[str]
    created_at: datetime
    edited_at: datetime

    def __init__(self,
                 id: str,
                 user_id: str,
                 name: str,
                 used_images: List[str],
                 created_at=None,
                 edited_at=None):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.used_images = used_images

        current_time = datetime.now()
        self.created_at = created_at if created_at is not None else current_time
        self.edited_at = edited_at if edited_at is not None else current_time

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'used_images': self.used_images,
            'created_at': self.created_at,
            'edited_at': self.edited_at
        }
