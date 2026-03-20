from typing import override

from sqlalchemy.orm import Session

from domain.entities.transaction import Transaction
from domain.repositories.base_repository import Repository
from domain.entities.transaction import Transaction, TransactionStatus
from infrastructure.models.transaction_model import TransactionModel

class TransactionRepository(Repository[Transaction]):   
    
    @override
    def get_all(self) -> list[Transaction]:
        models = self._db.query(TransactionModel).all()
        return [self._to_entity(model) for model in models]
    
    @override
    def save(self, transaction: Transaction) -> Transaction:
        model = TransactionModel(
            amount=transaction.amount,
            status=transaction.status.value
        )
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return self._to_entity(model)

    def _to_entity(self, model: TransactionModel) -> Transaction:
        return Transaction(
            id=model.id,
            amount=model.amount,
            status=TransactionStatus(model.status)
        )