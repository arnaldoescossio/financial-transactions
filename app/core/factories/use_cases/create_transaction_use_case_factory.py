from typing import Annotated

from fastapi import Depends

from app.core.factories.services.transaction_service_factory import (
    get_transaction_service,
)
from app.domain.service.transaction_service import TransactionService
from app.use_cases.transaction.create_transaction import CreateTransactionUseCase


def get_create_transaction_use_case(
    transaction_service: Annotated[
        TransactionService, Depends(get_transaction_service)
    ],
) -> CreateTransactionUseCase:
    return CreateTransactionUseCase(service=transaction_service)
