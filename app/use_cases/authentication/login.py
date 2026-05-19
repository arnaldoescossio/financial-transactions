from app.api.v1.schemas.auth_schema import LoginRequest, TokenResponse
from app.domain.entities.token import Token
from app.domain.service.auth_service import AuthService
from app.use_cases.base_use_case import UseCase


class LoginUseCase(UseCase[LoginRequest, TokenResponse, AuthService]):
    async def execute(
        self,
        login_request: LoginRequest,
        # auth_service: Annotated[AuthService | None, Depends(get_auth_service)],
    ) -> TokenResponse:
        token: Token = await self.service.login(
            login_request.email, login_request.password
        )

        # existing_user = await self.service.get_by_username(user_create.username)
        # if existing_user:
        #     raise UserAlreadyExistsException(user_create.username)

        # # Create a new user instance
        # new_user: User = await self.service.register(
        #     email=user_create.email,
        #     username=user_create.username,
        #     password=user_create.password,
        #     full_name=user_create.full_name,
        # )
        return TokenResponse(
            access_token=token.access_token,
            refresh_token=token.refresh_token,
        )
