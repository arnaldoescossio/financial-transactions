from typing import Sequence, override

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.domain.entities.account import Account
from app.domain.entities.transaction import Transaction
from app.domain.enums.transaction_status import TransactionStatus
from app.domain.ports.repositories.transaction_repository import (
    AbstractTransactionRepository,
)
from app.infrastructure.models.transaction_model import TransactionModel


class TransactionRepository(AbstractTransactionRepository):
    @override
    async def save(self, transaction: Transaction) -> Transaction:
        model: TransactionModel = self._to_model(transaction)
        self._db.add(model)
        await self._db.commit()
        await self._db.refresh(
            model, attribute_names=["account"]
        )  # Refresh to get the account relationship loaded
        return self._to_entity(model)

    async def get_by_account_id(
        self,
        account_id: int,
        transaction_status: TransactionStatus = TransactionStatus.SUCCESS,
    ) -> list[Transaction]:
        """Retrieve transactions by account ID and optional status.
            If status is not provided, it defaults to TransactionStatus.SUCCESS.

        Args:
            account_id (int): The ID of the account to retrieve transactions for.
            transaction_status (TransactionStatus, optional): Filter transactions by status. Defaults to TransactionStatus.SUCCESS.

        Returns:
            list[Transaction]: A list of transactions matching the criteria.
        """

        transactions: Sequence[TransactionModel] = (
            (
                await self._db.execute(
                    select(TransactionModel)
                    .where(
                        TransactionModel.account_id == account_id,
                        TransactionModel.status == transaction_status.value,
                    )
                    .options(selectinload(TransactionModel.account))
                )
            )
            .scalars()
            .all()
        )

        return [self._to_entity(model) for model in transactions]

    def _to_entity(self, model: TransactionModel) -> Transaction:
        return Transaction(
            id=model.id,
            amount=model.amount,
            status=TransactionStatus(model.status),
            account=Account(**model.account.__dict__) if model.account else None,
            account_id=model.account_id,
        )

    def _to_model(self, entity: Transaction) -> TransactionModel:
        return TransactionModel(
            id=entity.id,
            amount=entity.amount,
            status=entity.status.value,
            account_id=entity.account_id,
        )
