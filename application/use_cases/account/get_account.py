from typing import override

from application.use_cases.base_use_case import UseCase
from domain.entities.account import AccountResponse
from domain.exceptions.account_not_found import AccountNotFoundException
from infrastructure.models.account_model import AccountModel


class GetAccountUseCase(UseCase):
    """Use case for retrieving account details."""

    @override
    async def execute(self, account_id: int) -> AccountResponse:
        account: AccountModel | None = await self.repository.get_by_id(account_id)
        if not account:
            raise AccountNotFoundException("Account not found")
        
        transactions = [
            {
                "id": t.id,
                "amount": t.amount,
                "status": t.status
            }
            for t in account.transactions
        ]
        
        return AccountResponse(
            id=account.id,
            balance=account.balance,
            type=account.type,
            transactions=transactions
        )