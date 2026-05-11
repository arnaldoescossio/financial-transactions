from typing import Annotated

from fastapi import Depends

from app.core.factories.repositories.account_repository_factory import (
    get_account_repository,
)
from app.domain.ports.repositories.account_repository import AbstractAccountRepository
from app.domain.service.account_service import AccountService


def get_account_service(
    account_repository: Annotated[
        AbstractAccountRepository, Depends(get_account_repository)
    ],
) -> AccountService:
    """Factory for account service. Returns the repository for use case injection."""
    return AccountService(account_repository)
