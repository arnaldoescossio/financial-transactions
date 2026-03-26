from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import override

from domain.entities.account import AccountBase, AccountResponse
from domain.enums.transaction_status import TransactionStatus
from domain.repositories.base_repository import Repository
from infrastructure.models.account_model import AccountModel
from infrastructure.models.transaction_model import TransactionModel

class AccountRepository(Repository):
    """Repository for managing account data."""

    @override
    def save(self, account) -> AccountModel:
        """Create a new account in the repository."""
        model = AccountModel(
            balance=account.balance,
            type=account.type
        )
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return model
        # Implementation to save the account to the database or in-memory storage

    @override
    def get_by_id(self, account_id) -> AccountModel | None:
        return (
            self._db.execute(select(AccountModel).where(AccountModel.id == account_id)).scalars().first()
        )

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

    def _to_entity(self, model: AccountModel) -> AccountResponse:
        return AccountResponse(
            id=model.id,
            balance=model.balance,
            type=model.type,
            transactions=model.transactions
        )
