from typing import Protocol


class Texts(Protocol):
    START: str
    LANGUAGE: str
    CHOOSE_LANGUAGE: str
    MODE: str
    ALREADY_MAKE_REQUEST: str
    READY_FOR_NEW_REQUEST: str
    CLOSE: str

    @staticmethod
    def profile(subscription_type: str, current_model: str, daily_limits: dict) -> str:
        raise NotImplementedError

    @staticmethod
    def wait_for_another_request(seconds: int) -> str:
        raise NotImplementedError

    @staticmethod
    def processing_request() -> str:
        raise NotImplementedError
