"""Unit tests for authentication API routes."""

import uuid
from datetime import datetime
from unittest.mock import AsyncMock, Mock

import pytest

from app.api.v1.routes import auth_api
from app.api.v1.schemas.auth_schema import LoginRequest, RegisterRequest, TokenResponse
from app.api.v1.schemas.user_schema import UserResponse
from app.core.exceptions.user_exceptions import UserAlreadyExistsException
from app.domain.entities.user import UserRole, UserStatus


@pytest.mark.asyncio
async def test_register_endpoint_returns_user_response(monkeypatch):
    """Register route should delegate to use case and return created user."""
    register_data = RegisterRequest(
        email="newuser@example.com",
        username="newuser",
        password="SecurePass123!",
        full_name="New User",
    )

    expected = UserResponse(
        id=uuid.uuid4(),
        email="newuser@example.com",
        username="newuser",
        full_name="New User",
        role=UserRole.USER,
        status=UserStatus.ACTIVE,
        is_verified=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    fake_use_case = Mock()
    fake_use_case.execute = AsyncMock(return_value=expected)

    class FakeRegisterUserUseCase:
        def __init__(self, service):
            self.service = service

        async def execute(self, user_create):
            return await fake_use_case.execute(user_create)

    monkeypatch.setattr(auth_api, "RegisterUserUseCase", FakeRegisterUserUseCase)

    result = await auth_api.register(
        user_create=register_data,
        use_case=FakeRegisterUserUseCase(service=None),
    )

    assert isinstance(result, UserResponse)
    assert result.email == "newuser@example.com"
    assert result.username == "newuser"
    assert result.role == UserRole.USER
    fake_use_case.execute.assert_awaited_once_with(register_data)


@pytest.mark.asyncio
async def test_register_endpoint_calls_use_case_with_request_data(monkeypatch):
    """Register route should call use case with correct request data."""
    register_data = RegisterRequest(
        email="alice@example.com",
        username="alice_smith",
        password="AlicePass456!",
        full_name="Alice Smith",
    )

    created_user = UserResponse(
        id=uuid.uuid4(),
        email=register_data.email,
        username=register_data.username,
        full_name=register_data.full_name,
        role=UserRole.USER,
        status=UserStatus.ACTIVE,
        is_verified=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    fake_use_case = Mock()
    fake_use_case.execute = AsyncMock(return_value=created_user)

    class FakeRegisterUserUseCase:
        def __init__(self, service):
            self.service = service

        async def execute(self, user_create):
            return await fake_use_case.execute(user_create)

    monkeypatch.setattr(auth_api, "RegisterUserUseCase", FakeRegisterUserUseCase)

    await auth_api.register(
        user_create=register_data,
        use_case=FakeRegisterUserUseCase(service=None),
    )

    fake_use_case.execute.assert_awaited_once()
    called_request = fake_use_case.execute.call_args[0][0]
    assert called_request.email == "alice@example.com"
    assert called_request.username == "alice_smith"
    assert called_request.password == "AlicePass456!"


@pytest.mark.asyncio
async def test_register_endpoint_propagates_already_exists_exception(monkeypatch):
    """Register route should propagate UserAlreadyExistsException from use case."""
    register_data = RegisterRequest(
        email="existing@example.com",
        username="existinguser",
        password="SecurePass123!",
        full_name="Existing User",
    )

    fake_use_case = Mock()
    fake_use_case.execute = AsyncMock(
        side_effect=UserAlreadyExistsException("existing@example.com")
    )

    class FakeRegisterUserUseCase:
        def __init__(self, service):
            self.service = service

        async def execute(self, user_create):
            return await fake_use_case.execute(user_create)

    monkeypatch.setattr(auth_api, "RegisterUserUseCase", FakeRegisterUserUseCase)

    with pytest.raises(UserAlreadyExistsException):
        await auth_api.register(
            user_create=register_data,
            use_case=FakeRegisterUserUseCase(service=None),
        )

    fake_use_case.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_login_endpoint_returns_token_response(monkeypatch):
    """Login route should delegate to use case and return token."""
    login_data = LoginRequest(
        email="john@example.com",
        password="SecurePass123!",
    )

    expected = TokenResponse(
        access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U",
        refresh_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U",
        token_type="bearer",
    )

    fake_use_case = Mock()
    fake_use_case.execute = AsyncMock(return_value=expected)

    class FakeLoginUseCase:
        def __init__(self, service):
            self.service = service

        async def execute(self, login_request):
            return await fake_use_case.execute(login_request)

    monkeypatch.setattr(auth_api, "LoginUseCase", FakeLoginUseCase)

    result = await auth_api.login_json(
        body=login_data,
        use_case=FakeLoginUseCase(service=None),
    )

    assert isinstance(result, TokenResponse)
    assert result.access_token == expected.access_token
    assert result.refresh_token == expected.refresh_token
    assert result.token_type == "bearer"
    fake_use_case.execute.assert_awaited_once_with(login_data)


@pytest.mark.asyncio
async def test_login_endpoint_calls_use_case_with_credentials(monkeypatch):
    """Login route should call use case with correct credentials."""
    login_data = LoginRequest(
        email="alice@example.com",
        password="AlicePass456!",
    )

    token = TokenResponse(
        access_token="access_token_xyz",
        refresh_token="refresh_token_xyz",
        token_type="bearer",
    )

    fake_use_case = Mock()
    fake_use_case.execute = AsyncMock(return_value=token)

    class FakeLoginUseCase:
        def __init__(self, service):
            self.service = service

        async def execute(self, login_request):
            return await fake_use_case.execute(login_request)

    monkeypatch.setattr(auth_api, "LoginUseCase", FakeLoginUseCase)

    await auth_api.login_json(
        body=login_data,
        use_case=FakeLoginUseCase(service=None),
    )

    fake_use_case.execute.assert_awaited_once()
    called_request = fake_use_case.execute.call_args[0][0]
    assert called_request.email == "alice@example.com"
    assert called_request.password == "AlicePass456!"


@pytest.mark.asyncio
async def test_login_endpoint_response_includes_bearer_token_type(monkeypatch):
    """Login response should include token_type set to 'bearer'."""
    login_data = LoginRequest(
        email="user@example.com",
        password="Password123!",
    )

    expected = TokenResponse(
        access_token="access_token_abc",
        refresh_token="refresh_token_abc",
        token_type="bearer",
    )

    fake_use_case = Mock()
    fake_use_case.execute = AsyncMock(return_value=expected)

    class FakeLoginUseCase:
        def __init__(self, service):
            self.service = service

        async def execute(self, login_request):
            return await fake_use_case.execute(login_request)

    monkeypatch.setattr(auth_api, "LoginUseCase", FakeLoginUseCase)

    result = await auth_api.login_json(
        body=login_data,
        use_case=FakeLoginUseCase(service=None),
    )

    assert hasattr(result, "token_type")
    assert result.token_type == "bearer"


@pytest.mark.asyncio
async def test_register_endpoint_response_has_user_fields(monkeypatch):
    """Register response should have all user fields."""
    register_data = RegisterRequest(
        email="newuser@example.com",
        username="newuser",
        password="SecurePass123!",
        full_name="New User",
    )

    user_id = uuid.uuid4()
    expected = UserResponse(
        id=user_id,
        email="newuser@example.com",
        username="newuser",
        full_name="New User",
        role=UserRole.USER,
        status=UserStatus.ACTIVE,
        is_verified=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    fake_use_case = Mock()
    fake_use_case.execute = AsyncMock(return_value=expected)

    class FakeRegisterUserUseCase:
        def __init__(self, service):
            self.service = service

        async def execute(self, user_create):
            return await fake_use_case.execute(user_create)

    monkeypatch.setattr(auth_api, "RegisterUserUseCase", FakeRegisterUserUseCase)

    result = await auth_api.register(
        user_create=register_data,
        use_case=FakeRegisterUserUseCase(service=None),
    )

    assert hasattr(result, "id")
    assert hasattr(result, "email")
    assert hasattr(result, "username")
    assert hasattr(result, "full_name")
    assert hasattr(result, "role")
    assert hasattr(result, "status")
    assert hasattr(result, "is_verified")
    assert hasattr(result, "created_at")
    assert hasattr(result, "updated_at")


@pytest.mark.asyncio
async def test_login_endpoint_response_has_token_fields(monkeypatch):
    """Login response should have all token fields."""
    login_data = LoginRequest(
        email="user@example.com",
        password="Password123!",
    )

    expected = TokenResponse(
        access_token="access_token_xyz",
        refresh_token="refresh_token_xyz",
        token_type="bearer",
    )

    fake_use_case = Mock()
    fake_use_case.execute = AsyncMock(return_value=expected)

    class FakeLoginUseCase:
        def __init__(self, service):
            self.service = service

        async def execute(self, login_request):
            return await fake_use_case.execute(login_request)

    monkeypatch.setattr(auth_api, "LoginUseCase", FakeLoginUseCase)

    result = await auth_api.login_json(
        body=login_data,
        use_case=FakeLoginUseCase(service=None),
    )

    assert hasattr(result, "access_token")
    assert hasattr(result, "refresh_token")
    assert hasattr(result, "token_type")
    assert len(result.access_token) > 0
    assert len(result.refresh_token) > 0
