from abc import abstractmethod

from app.domain.entities.transaction import Transaction
from app.domain.ports.repositories.base_repository import Repository
from app.infrastructure.models.transaction_model import TransactionModel


class AbstractTransactionRepository(Repository[Transaction, TransactionModel]):
    """Port (interface) for transaction persistence — no infrastructure details."""

    @abstractmethod
    async def save(self, transaction: Transaction) -> Transaction: ...

    @abstractmethod
    async def get_by_account_id(
        self, account_id: int, transaction_status: str
    ) -> list[Transaction]: ...
