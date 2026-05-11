from abc import abstractmethod
from asyncio import Protocol

from sqlalchemy.ext.asyncio import AsyncSession


class Repository[E, M](Protocol):
    def __init__(self, db: AsyncSession) -> None:
        self._db: AsyncSession = db

    @abstractmethod
    def _to_entity(self, model: M) -> E: ...

    @abstractmethod
    def _to_model(self, entity: E) -> M: ...