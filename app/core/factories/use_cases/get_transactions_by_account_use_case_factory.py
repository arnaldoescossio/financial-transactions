from typing import Annotated

from fastapi import Depends

from app.core.factories.services.transaction_service_factory import get_transaction_service
from app.domain.service.transaction_service import TransactionService
from app.use_cases.transaction.get_transactions_by_account import (
    GetTransactionsByAccountUseCase,
)


def get_get_transactions_by_account_use_case(
    transaction_service: Annotated[
        TransactionService, Depends(get_transaction_service)
    ],
) -> GetTransactionsByAccountUseCase:
    return GetTransactionsByAccountUseCase(service=transaction_service)
