from typing import Annotated

from fastapi import Depends

from app.core.factories.repositories.user_repository_factory import get_user_repository
from app.domain.ports.repositories.user_repository import AbstractUserRepository
from app.domain.service.auth_service import AuthService


def get_auth_service(
    user_repository: Annotated[AbstractUserRepository, Depends(get_user_repository)],
) -> AuthService:
    return AuthService(user_repository)
