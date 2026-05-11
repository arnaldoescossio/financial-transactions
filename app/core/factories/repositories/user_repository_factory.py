from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.adapters.repositories.user_repository import UserDatabaseRepository
from app.infrastructure.database import get_db

def get_user_repository(
        session: Annotated[AsyncSession, Depends(get_db)],
):
    """Factory for user repository."""
    return UserDatabaseRepository(session)