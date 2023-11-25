from typing import Dict, Type

from . import en
from .texts import Texts

localization_classes: Dict[str, Type[Texts]] = {
    'en': en.English,
}


def get_localization(language_code: str) -> Texts:
    localization_class = localization_classes.get(language_code, en.English)
    return localization_class()
