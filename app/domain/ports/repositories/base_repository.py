from asyncio import Protocol

from sqlalchemy.ext.asyncio import AsyncSession


class Repository(Protocol):
    def __init__(self, db: AsyncSession) -> None:
        self._db: AsyncSession = db
