from typing import Annotated

from fastapi import Depends

from app.core.factories.repositories.transaction_repository_factory import (
    get_transaction_repository,
)
from app.domain.ports.repositories.transaction_repository import (
    AbstractTransactionRepository,
)
from app.domain.service.transaction_service import TransactionService


def get_transaction_service(
    transaction_repository: Annotated[
        AbstractTransactionRepository, Depends(get_transaction_repository)
    ],
) -> TransactionService:
    """Factory for transaction service. Returns the repository for use case injection."""
    return TransactionService(transaction_repository)
