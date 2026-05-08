from typing import override

from app.api.v1.schemas.account_schema import AccountCreate, AccountResponse
from app.infrastructure.adapters.repositories.account_repository import AccountRepository
from app.use_cases.base_use_case import UseCase


class CreateAccountUseCase(UseCase[AccountCreate, AccountResponse, AccountRepository]):  # noqa: F821
    """Use case for creating a new account."""

    @override
    async def execute(self, account: AccountCreate) -> AccountResponse:
        """Create a new account.

        Args:
            account: The account data to create

        Returns:
            The created account entity
        """

        account = await self.repository.save(account)

        return AccountResponse(
            id=account.id,
            balance=account.balance,
            type=account.type,
        )
