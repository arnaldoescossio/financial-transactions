from abc import abstractmethod

from pytest import Session
from domain.entities.transaction import TransactionBase


class Repository[E]:
    
    def __init__(self, db: Session):
        self._db = db

    @abstractmethod
    def get_all(self) -> list[E]:
        """Retrieve all entities from the repository."""
        # Implementation to retrieve all entities from the database or in-memory storage
        pass

    @abstractmethod
    def get_by_id(self, entity_id: int) -> E:
        """Retrieve an entity by its ID."""
        # Implementation to retrieve an entity by its ID from the database or in-memory storage
        pass
    
    @abstractmethod
    def save(self, entity: E) -> E:
        """Create a new entity in the repository."""
        # Implementation to save the entity to the database or in-memory storage
        pass