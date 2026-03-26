from application.use_cases.base_use_case import UseCase
from domain.entities.account import AccountResponse

from application.config.logging_config import logger
from domain.entities.account import AccountResponse
from domain.exceptions.account_not_found import AccountNotFoundException

class GetAccountUseCase(UseCase):

    def execute(self, account_id: int) -> AccountResponse:
        account = self.repository.get_by_id(account_id)
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