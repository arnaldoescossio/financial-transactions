from abc import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class Repository[E]:
    def __init__(self, db: AsyncSession):
        self._db = db

    @abstractmethod
    async def get_by_id(self, entity_id: int) -> E:
        """Retrieve an entity by its ID."""
        # Implementation to retrieve an entity by its ID from the database or in-memory storage
        pass

    @abstractmethod
    async def save(self, entity: E) -> E:
        """Create a new entity in the repository."""
        # Implementation to save the entity to the database or in-memory storage
        pass
