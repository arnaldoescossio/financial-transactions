from typing import override

from application.use_cases.base_use_case import UseCase
from domain.entities.account import AccountCreate, AccountResponse


class CreateAccountUseCase(UseCase):
    """Use case for creating a new account."""
    
    @override
    async def execute(self, account: AccountCreate) -> AccountResponse:
        """Create a new account.
        
        Args:
            dto: The data transfer object containing account information
            
        Returns:
            The created account entity
            
        Raises:
            ValueError: If the account data is invalid
        """
        
        account = await self.repository.save(account)

        return AccountResponse(
            id=account.id,
            balance=account.balance,
            type=account.type,
        )