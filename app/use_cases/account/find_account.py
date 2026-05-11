from typing import override

from app.api.v1.schemas.account_schema import AccountCreate, AccountResponse
from app.core.exceptions.account_exceptions import AccountNotFoundException
from app.domain.entities.account import Account
from app.domain.service.account_service import AccountService
from app.use_cases.base_use_case import UseCase


class FindAccountUseCase(UseCase[AccountCreate, AccountResponse, AccountService]):
    """Use case for retrieving account details."""

    @override
    async def execute(self, account_id: int) -> AccountResponse:
        account: Account | None = await self.service.get_by_id(account_id)
        if not account:
            raise AccountNotFoundException("Account not found")

        transactions = [
            {"id": t.id, "amount": t.amount, "status": t.status}
            for t in account.transactions
        ]

        return AccountResponse(
            id=account.id,
            balance=account.balance,
            type=account.type,
            transactions=transactions,
        )
