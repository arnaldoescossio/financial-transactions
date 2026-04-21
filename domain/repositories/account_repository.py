from typing import Tuple, override

from sqlalchemy import Result, select
from sqlalchemy.orm import selectinload

from domain.repositories.base_repository import Repository
from infrastructure.models.account_model import AccountModel


class AccountRepository(Repository[AccountModel]):
    """Repository for managing account data."""

    @override
    async def save(self, account) -> AccountModel:
        """Create a new account in the repository."""
        model = AccountModel(balance=account.balance, type=account.type)
        self._db.add(model)
        await self._db.commit()
        await self._db.refresh(model)
        return model

    @override
    async def get_by_id(self, account_id) -> AccountModel | None:
        result: Result[Tuple[AccountModel]]   = await self._db.execute(
            select(AccountModel)
            .where(AccountModel.id == account_id)
            .options(selectinload(AccountModel.transactions))
        )
        return result.scalar()

    # @abstractmethod
    # def update(self, account):
    #     """Update an existing account in the repository."""
    #     # Implementation to update the account in the database or in-memory storage
    #     pass

    # @override
    # def delete(self, account_id):
    #     """Delete an account by its ID."""
    #     # Implementation to delete the account from the database or in-memory storage
    #     pass

    # def _to_entity(self, model: AccountModel) -> AccountResponse:
    #     return AccountResponse(
    #         id=model.id,
    #         balance=model.balance,
    #         type=model.type,
    #         transactions=model.transactions
    #     )
