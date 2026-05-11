from typing import override

from app.api.v1.schemas.account_schema import AccountCreate, AccountResponse
from app.domain.entities.account import Account
from app.domain.service.account_service import AccountService
from app.use_cases.base_use_case import UseCase


class CreateAccountUseCase(UseCase[AccountCreate, AccountResponse, AccountService]):
    """Use case for creating a new account."""

    @override
    async def execute(self, account_data: AccountCreate) -> AccountResponse:
        """Create a new account.

        Args:
            account_data: The account data to create

        Returns:
            The created account entity
        """
        # Convert schema to entity
        account = Account(balance=account_data.balance, type=account_data.type)
        created_account = await self.service.save(account)

        return AccountResponse(
            id=created_account.id,
            balance=created_account.balance,
            type=created_account.type,
            transactions=created_account.transactions,
        )
