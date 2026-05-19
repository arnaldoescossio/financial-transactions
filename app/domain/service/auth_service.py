from typing import Optional

from app.core.exceptions.user_exceptions import InactiveUserException
from app.core.exceptions.auth_exceptions import CredentialsException
from app.domain.entities.token import Token
from app.domain.entities.user import User, UserRole
from app.domain.ports.repositories.user_repository import AbstractUserRepository
from app.infrastructure.security.password import hash_password, verify_password
from app.infrastructure.security.jwt import jwt_service


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
    
    async def login(self, email: str, password: str) -> Token:
        user = await self._users.get_by_email(email)
        
        if not user or not verify_password(password, user.hashed_password):
            raise CredentialsException("Invalid email or password.")
        if not user.is_active:
            raise InactiveUserException()
        
        return await self._issue_pair(user)

    # ------------------------------------------------------------------ #
    #  Private                                                             #
    # ------------------------------------------------------------------ #

    async def _issue_pair(self, user: User) -> Token:
        access_token,  _           = jwt_service.create_access_token(str(user.id), user.role)
        refresh_token, refresh_jti = jwt_service.create_refresh_token(str(user.id))

        # await self._tokens.store_refresh(
        #     jti=refresh_jti,
        #     user_id=str(user.id),
        #     ttl_seconds=jwt_service.refresh_token_ttl_seconds,
        # )
        return Token(access_token=access_token, refresh_token=refresh_token)
        
