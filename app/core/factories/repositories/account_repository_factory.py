from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.adapters.repositories.account_repository import (
    AccountRepository,
)
from app.infrastructure.database import get_db


def get_account_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> AccountRepository:
    """Factory for account repository."""
    return AccountRepository(session)
