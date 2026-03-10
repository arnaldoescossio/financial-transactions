from application.use_cases.base_use_case import UseCase
from application.use_cases.enums.transaction_use_case_type import TransactionUseCaseType
from domain.repositories.transaction_repository import TransactionRepository


class UseCaseFactory:
    """Factory class for creating use case instances.
    
    This factory uses the TransactionUseCaseType enum to instantiate
    the appropriate use case based on the specified type.
    """

    @staticmethod
    def create(
        use_case_type: TransactionUseCaseType,
        repository: TransactionRepository
    ) -> UseCase:
        """Create a use case instance based on the specified type.
        
        Args:
            use_case_type: The type of use case to create
            repository: The transaction repository dependency
            
        Returns:
            An instance of the requested use case
            
        Raises:
            ValueError: If the use case type is not supported
        """
        if not isinstance(use_case_type, TransactionUseCaseType):
            raise ValueError(f"Invalid use case type: {use_case_type}")
        
        return use_case_type.use_case_class(repository)
