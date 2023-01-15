from abc import ABC, abstractmethod


class SmsSender(ABC):

    @abstractmethod
    def send_login_sms(self, code: str, number: str, hash_str:str) -> None:
        pass

    @abstractmethod
    def send_signup_sms(self, code: str, number: str, hash_str:str) -> None:
        pass

    @abstractmethod
    def send_sms(self):
        pass
