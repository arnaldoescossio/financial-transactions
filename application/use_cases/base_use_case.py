from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class UseCase(ABC, Generic[T]):
    """Abstract base class for all use cases.
    
    All use cases must implement the execute method which contains the business logic.
    """

    @abstractmethod
    def execute(self, data) -> T:
        """Execute the use case logic and return the result.
        
        Returns:
            The result of the use case execution.
        """
        pass
