from abc import abstractmethod
from typing import Optional

from app.domain.entities.account import Account
from app.domain.ports.repositories.base_repository import Repository
from app.infrastructure.models.account_model import AccountModel


class AbstractAccountRepository(Repository[Account, AccountModel]):
    """Port (interface) for account persistence — no infrastructure details."""

    @abstractmethod
    async def save(self, account: Account) -> Account: ...

    @abstractmethod
    async def get_by_id(self, account_id: int) -> Optional[Account]: ...
