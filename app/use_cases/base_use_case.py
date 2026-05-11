from asyncio import Protocol


class UseCase[D, R, S](Protocol):
    """Abstract base class for all use cases.

    All use cases must implement the execute method which contains the business logic.
    """

    def __init__(self, service: S) -> None:
        self.service: S = service

    async def execute(self, data: D) -> R:
        """Execute the use case logic and return the result.

        Returns:
            The result of the use case execution.
        """
        pass
