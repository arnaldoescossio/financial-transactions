from application.dtos.create_account_dto import CreateAccountDTO
from application.use_cases.base_use_case import UseCase
from domain.entities.account import Account
from domain.repositories.account_repository import AccountRepository


class CreateAccountUseCase(UseCase[CreateAccountDTO]):
    """Use case for creating a new account."""
    
    def __init__(self, repository: AccountRepository):
        super().__init__(repository)
    
    def execute(self, dto: CreateAccountDTO) -> CreateAccountDTO:
        """Create a new account.
        
        Args:
            dto: The data transfer object containing account information
            
        Returns:
            The created account entity
            
        Raises:
            ValueError: If the account data is invalid
        """
        account = dto.to_entity()
        
        account = self.repository.save(account)
        return CreateAccountDTO.from_entity(account)