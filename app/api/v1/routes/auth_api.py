from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.v1.schemas.auth_schema import LoginRequest, RegisterRequest, TokenResponse
from app.api.v1.schemas.user_schema import UserResponse
from app.core.config.logging_config import logger
from app.core.factories.use_cases.login_use_case_factory import get_login_use_case
from app.core.factories.use_cases.register_use_case_factory import get_register_use_case
from app.use_cases.authentication.login import LoginUseCase
from app.use_cases.authentication.register_user import RegisterUserUseCase

router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    user_create: RegisterRequest,
    use_case: Annotated[RegisterUserUseCase, Depends(get_register_use_case)],
) -> UserResponse:
    logger.info(f"Admin is registering a new user with email {user_create.email}")
    user: UserResponse = await use_case.execute(user_create=user_create)
    return UserResponse.model_validate(user)


@router.post("/login", response_model=TokenResponse)
async def login_json(
    body: LoginRequest,
    use_case: Annotated[LoginUseCase, Depends(get_login_use_case)],
) -> TokenResponse:
    """Login via JSON body — returns access + refresh tokens."""
    logger.info(f"User with email {body.email} is attempting to log in.")

    token: TokenResponse = await use_case.execute(login_request=body)
    return TokenResponse.model_validate(token)
