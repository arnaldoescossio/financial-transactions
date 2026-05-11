from typing import Optional

from app.domain.entities.user import User, UserRole
from app.domain.ports.repositories.user_repository import AbstractUserRepository
from app.infrastructure.security.password import hash_password


class AuthService:
    """
    Orchestrates authentication flows.
    Depends on AbstractUserRepository and AbstractTokenRepository (ports),
    never on concrete infrastructure classes.
    """

    def __init__(
        self,
        user_repo: AbstractUserRepository,
        # token_repo: AbstractTokenRepository,
    ) -> None:
        self._users: AbstractUserRepository = user_repo
        # self._tokens = token_repo

    async def register(
        self,
        email: str,
        username: str,
        password: str,
        full_name: str | None = None,
        role: UserRole = UserRole.USER,
    ) -> User:
        """
        Register a new user.

        Args:
            email: User email address
            username: Unique username
            password: Plain text password (will be hashed)
            full_name: Optional full name
            role: User role (default: USER)
        Returns:
            The created User entity
        """
        hashed_password = hash_password(password)
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
            full_name=full_name,
            role=role,
        )
        created_user: User = await self._users.create(user)
        return created_user

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self._users.get_by_email(email)

    async def get_by_username(self, username: str) -> Optional[User]:
        return await self._users.get_by_username(username)