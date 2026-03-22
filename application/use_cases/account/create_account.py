from application.use_cases.base_use_case import UseCase
from domain.entities.account import Account, AccountCreate
from domain.repositories.account_repository import AccountRepository


class CreateAccountUseCase(UseCase):
    """Use case for creating a new account."""
    
    def __init__(self, repository: AccountRepository):
        super().__init__(repository)
    
    def execute(self, dto: AccountCreate) -> Account:
        """Create a new account.
        
        Args:
            dto: The data transfer object containing account information
            
        Returns:
            The created account entity
            
        Raises:
            ValueError: If the account data is invalid
        """
        account = Account(
            id=None,
            balance=dto.balance
        )
        
        return self.repository.save(account)