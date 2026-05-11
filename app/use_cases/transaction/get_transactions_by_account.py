from typing import override

from app.api.v1.schemas.transaction_schema import TransactionBase, TransactionResponse
from app.core.config.logging_config import logger
from app.domain.entities.transaction import Transaction
from app.domain.enums.transaction_status import TransactionStatus
from app.domain.service.transaction_service import TransactionService
from app.use_cases.base_use_case import UseCase


class GetTransactionsByAccountUseCase(
    UseCase[dict, list[TransactionResponse], TransactionService]
):
    @override
    async def execute(
        self,
        params: dict,
    ) -> list[TransactionResponse]:
        account_id: int = params.get("account_id")
        transaction_status: TransactionStatus = params.get(
            "transaction_status", TransactionStatus.SUCCESS
        )
        transactions: list[
            Transaction
        ] = await self.service.get_transactions_by_account_id(
            account_id, transaction_status
        )
        logger.info(
            f"Retrieved {len(transactions)} transactions for account {account_id}"
        )

        return list[TransactionResponse](
            TransactionResponse(
                id=t.id,
                amount=t.amount,
                status=t.status,
                account=None,  # We don't need the account details here
            )
            for t in transactions
        )
