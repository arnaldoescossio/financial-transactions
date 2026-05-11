from typing import Optional, Tuple, override

from sqlalchemy import Result, select
from sqlalchemy.orm import selectinload

from app.domain.entities.account import Account
from app.domain.entities.transaction import Transaction
from app.domain.ports.repositories.account_repository import AbstractAccountRepository
from app.infrastructure.models.account_model import AccountModel


class AccountRepository(AbstractAccountRepository):
    """Repository for managing account data."""

    @override
    async def save(self, account: Account) -> Account:
        """Create a new account in the repository."""
        model = AccountModel(balance=account.balance, type=account.type)
        self._db.add(model)
        await self._db.commit()
        await self._db.refresh(
            model, attribute_names=["transactions"]
        ) 
        return self._to_entity(model)

    @override
    async def get_by_id(self, account_id: int) -> Optional[Account]:
        result: Result[Tuple[AccountModel]] = await self._db.execute(
            select(AccountModel)
            .where(AccountModel.id == account_id)
            .options(selectinload(AccountModel.transactions))
        )
        model: AccountModel | None = result.scalar()
        return self._to_entity(model)

    def _to_entity(self, model: AccountModel) -> Optional[Account]:
        return (
            Account(
                id=model.id,
                balance=model.balance,
                type=model.type,
                transactions= [Transaction(**trans.__dict__) for trans in model.transactions] if model.transactions else [],
            )
            if model
            else None
        )

    def _to_model(self, account: Account) -> AccountModel:
        return AccountModel(
            id=account.id,
            balance=account.balance,
            type=account.type,
        )
