from abc import ABC, abstractmethod

class UseCase[D, A, R](ABC):
    """Abstract base class for all use cases.

    All use cases must implement the execute method which contains the business logic.
    """

    def __init__(self, repository: R) -> None:
        self.repository: R = repository

    @abstractmethod
    def execute(self, data: D) -> A:
        """Execute the use case logic and return the result.

        Returns:
            The result of the use case execution.
        """
        pass
