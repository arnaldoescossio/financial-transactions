from pydantic import BaseModel
from decimal import Decimal

from domain.entities.transaction import Transaction
from domain.enums.transaction_status import TransactionStatus


class CreateTransactionDTO(BaseModel):
    amount: float
    status: str

    class Config:
        from_attributes = True

    def to_entity(self):
        return Transaction(            
            id=None,
            amount=self.amount,
            status=TransactionStatus(self.status)
        )
    
    @staticmethod
    def from_entity(entity):
        return CreateTransactionDTO(
            amount=float(entity.amount),
            status=entity.status.value
        )
