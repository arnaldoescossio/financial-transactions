from abc import abstractmethod

from domain.repositories.base_repository import Repository


class UseCase[D]:
    """Abstract base class for all use cases.
    
    All use cases must implement the execute method which contains the business logic.
    """
    def __init__(self, repository: Repository):
        self.repository = repository
    
    @abstractmethod
    def execute(self, data: D) -> D:
        """Execute the use case logic and return the result.
        
        Returns:
            The result of the use case execution.
        """
        pass
