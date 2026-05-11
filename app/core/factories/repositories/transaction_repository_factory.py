from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.adapters.repositories.transaction_repository import TransactionRepository
from app.infrastructure.database import get_db


def get_transaction_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> TransactionRepository:
    """Factory for transaction repository."""
    return TransactionRepository(session)
