from dataclasses import dataclass

from application.dtos.base_dto import Dto
from domain.entities.transaction import Transaction
from domain.enums.transaction_status import TransactionStatus

@dataclass
class CreateTransactionDTO(Dto):
    amount: float
    status: str

    def to_entity(self) -> Transaction:
        return Transaction(            
            id=None,
            amount=self.amount,
            status=TransactionStatus(self.status)
        )
    
    @staticmethod
    def from_entity(entity) -> 'CreateTransactionDTO':
        return CreateTransactionDTO(
            amount=float(entity.amount),
            status=entity.status.value
        )
