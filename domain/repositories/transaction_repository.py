from typing import Sequence, override

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from domain.entities.transaction import TransactionCreate
from domain.enums.transaction_status import TransactionStatus
from domain.repositories.base_repository import Repository
from infrastructure.models.transaction_model import TransactionModel


class TransactionRepository(Repository[TransactionModel]):
    @override
    async def save(self, transaction: TransactionCreate) -> TransactionModel:
        model = TransactionModel(
            amount=transaction.amount,
            status=transaction.status.value,
            account_id=transaction.account_id,
        )
        self._db.add(model)
        await self._db.commit()
        await self._db.refresh(model, attribute_names=["account"])  # Refresh to get the account relationship loaded
        return model

    async def get_by_account_id(
        self,
        account_id: int,
        transaction_status: TransactionStatus = TransactionStatus.SUCCESS,
    ) -> list[TransactionModel]:
        """Retrieve transactions by account ID and optional status.
            If status is not provided, it defaults to TransactionStatus.SUCCESS.

        Args:
            account_id (int): The ID of the account to retrieve transactions for.
            transaction_status (TransactionStatus, optional): Filter transactions by status. Defaults to TransactionStatus.SUCCESS.

        Returns:
            list[TransactionModel]: A list of transactions matching the criteria.
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

        return transactions
