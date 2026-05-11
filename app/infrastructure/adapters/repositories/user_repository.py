from typing import Optional
import uuid

from sqlalchemy import delete, func, select

from app.domain.entities.user import User
from app.domain.ports.repositories.user_repository import AbstractUserRepository
from app.infrastructure.models.user_model import UserModel


class UserDatabaseRepository(AbstractUserRepository):
    """Concrete implementation of AbstractUserRepository using a SQL database."""

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        result = await self._db.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalars().first()
        return self._to_domain(model)

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self._db.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalars().first()
        return self._to_domain(model)

    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self._db.execute(
            select(UserModel).where(UserModel.username == username)
        )
        model = result.scalars().first()
        return self._to_domain(model)

    async def create(self, user: User) -> User:
        model = self._to_model(user)
        self._db.add(model)
        await self._db.commit()
        await self._db.refresh(model)
        return self._to_domain(model)

    async def update(self, user: User) -> User:
        model = self._to_model(user)
        await self._db.merge(model)
        await self._db.commit()
        await self._db.refresh(model)
        return self._to_domain(model)

    async def delete(self, user_id: uuid.UUID) -> None:
        await self._db.execute(delete(UserModel).where(UserModel.id == user_id))
        await self._db.commit()

    async def exists_by_email(self, email: str) -> bool:
        result = await self._db.execute(
            select(func.count()).select_from(UserModel).where(UserModel.email == email)
        )
        return result.scalar_one() > 0

    @staticmethod
    def _to_domain(model: UserModel) -> Optional[User]:
        return User.model_validate(model) if model else None

    @staticmethod
    def _to_model(user: User) -> UserModel:
        return UserModel(
            id=user.id,
            email=user.email,
            username=user.username,
            hashed_password=user.hashed_password,
            full_name=user.full_name,
            role=user.role,
            status=user.status,
            is_verified=user.is_verified,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
