from abc import ABC, abstractmethod
from domain.entities.transaction import Transaction


class TransactionRepository(ABC):
    
    @abstractmethod
    def get_all(self) -> list[Transaction]:
        pass