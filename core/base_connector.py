# core/base_connector.py
from abc import ABC, abstractmethod

class BaseLLMConnector(ABC):
    @abstractmethod
    def connect(self) -> bool:
        pass

    @abstractmethod
    def send_query(self, prompt: str) -> str:
        pass