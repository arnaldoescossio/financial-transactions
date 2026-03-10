from sqlalchemy.orm import Session
from domain.entities.transaction import Transaction, TransactionStatus
from domain.repositories.transaction_repository import TransactionRepository
from infrastructure.models.transaction_model import TransactionModel

class PostgresTransactionRepository(TransactionRepository):

    def __init__(self, db: Session):
        self._db = db

    def get_all(self) -> list[Transaction]:
        models = self._db.query(TransactionModel).all()
        return [self._to_entity(model) for model in models]
        # return [self._to_entity(model) for model in transaction_models]
    
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