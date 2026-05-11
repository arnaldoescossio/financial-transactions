from typing import Annotated

from fastapi import Depends

from app.core.factories.services.auth_service_factory import get_auth_service
from app.domain.service.auth_service import AuthService
from app.use_cases.authentication.register_user import RegisterUserUseCase


def get_register_use_case(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> RegisterUserUseCase:
    return RegisterUserUseCase(service=auth_service)
