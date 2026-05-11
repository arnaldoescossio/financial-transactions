from app.domain.entities.transaction import Transaction
from app.domain.enums.transaction_status import TransactionStatus
from app.domain.ports.repositories.transaction_repository import (
    AbstractTransactionRepository,
)


class TransactionService:
    """
    Orchestrates transaction-related flows.
    Depends on AbstractTransactionRepository (port),
    never on concrete infrastructure classes.
    """

    def __init__(
        self,
        transaction_repo: AbstractTransactionRepository,
        # token_repo: AbstractTokenRepository,
    ) -> None:
        self._transactions: AbstractTransactionRepository = transaction_repo
        # self._tokens = token_repo

    async def save(
        self,
        transaction: Transaction,
    ) -> Transaction:

        created_transaction: Transaction = await self._transactions.save(transaction)
        return created_transaction

    async def get_transactions_by_account_id(
        self,
        account_id: int,
        transaction_status: TransactionStatus = TransactionStatus.SUCCESS,
    ) -> list[Transaction]:
        return await self._transactions.get_by_account_id(
            account_id, transaction_status
        )
