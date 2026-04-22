from typing import override

from app.config.logging_config import logger
from app.domain.entities.transaction import TransactionBase
from app.domain.enums.transaction_status import TransactionStatus
from app.use_cases.base_use_case import UseCase


class GetTransactionsByAccountUseCase(UseCase):
    @override
    async def execute(
        self,
        account_id: int,
        transaction_status: TransactionStatus = TransactionStatus.SUCCESS,
    ) -> list[TransactionBase]:
        transactions = await self.repository.get_by_account_id(
            account_id, transaction_status
        )
        logger.info(
            f"Retrieved {len(transactions)} transactions for account {account_id}"
        )

        return list[TransactionBase](
            TransactionBase(
                id=t.id,
                amount=t.amount,
                status=t.status,
            )
            for t in transactions
        )
