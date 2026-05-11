from app.api.v1.schemas.auth_schema import RegisterRequest
from app.api.v1.schemas.user_schema import UserResponse
from app.core.exceptions.user_exceptions import UserAlreadyExistsException
from app.domain.entities.user import User
from app.domain.service.auth_service import AuthService
from app.use_cases.base_use_case import UseCase


class RegisterUserUseCase(UseCase[RegisterRequest, UserResponse, AuthService]):
    async def execute(
        self,
        user_create: RegisterRequest,
        # auth_service: Annotated[AuthService | None, Depends(get_auth_service)],
    ) -> UserResponse:
        # Check if the email and username are already registered
        existing_user = await self.service.get_by_email(user_create.email)
        if existing_user:
            raise UserAlreadyExistsException(user_create.email)

        existing_user = await self.service.get_by_username(user_create.username)
        if existing_user:
            raise UserAlreadyExistsException(user_create.username)

        # Create a new user instance
        new_user: User = await self.service.register(
            email=user_create.email,
            username=user_create.username,
            password=user_create.password,
            full_name=user_create.full_name,
        )

        return UserResponse.model_validate(new_user)
