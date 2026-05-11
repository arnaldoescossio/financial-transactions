import uuid
from abc import abstractmethod

from alembic.environment import Optional

from app.domain.entities.user import User
from app.domain.ports.repositories.base_repository import Repository
from app.infrastructure.models.user_model import UserModel


class AbstractUserRepository(Repository[User, UserModel]):
    """Port (interface) for user persistence — no infrastructure details."""

    @abstractmethod
    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]: ...

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]: ...

    @abstractmethod
    async def create(self, user: User) -> User: ...

    @abstractmethod
    async def update(self, user: User) -> User: ...

    @abstractmethod
    async def delete(self, user_id: uuid.UUID) -> None: ...

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool: ...
