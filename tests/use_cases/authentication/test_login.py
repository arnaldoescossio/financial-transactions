"""Unit tests for LoginUseCase."""

from unittest.mock import AsyncMock, Mock

import pytest

from app.api.v1.schemas.auth_schema import LoginRequest, TokenResponse
from app.domain.entities.token import Token
from app.domain.service.auth_service import AuthService
from app.use_cases.authentication.login import LoginUseCase


@pytest.fixture
def mock_service():
    """Create a mock auth service for testing."""
    return Mock(spec=AuthService)


@pytest.fixture
def login_request():
    """Create sample login request data for testing."""
    return LoginRequest(
        email="john@example.com",
        password="SecurePass123!",
    )


@pytest.fixture
def sample_token():
    """Create a sample token entity for testing."""
    return Token(
        access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZmYwNGU2Ny0yOTE3LTQwYjQtOGE5Yi04ZTUwNzEyNDYwYjMiLCJleHAiOjE3NDc4MzU1NTR9.hashed_access_token",
        refresh_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZmYwNGU2Ny0yOTE3LTQwYjQtOGE5Yi04ZTUwNzEyNDYwYjMiLCJleHAiOjE3NDcxNjE1NTR9.hashed_refresh_token",
    )


@pytest.mark.asyncio
async def test_login_success(mock_service, login_request, sample_token):
    """Test successful login returns TokenResponse."""
    # Arrange
    mock_service.login = AsyncMock(return_value=sample_token)
    use_case = LoginUseCase(mock_service)

    # Act
    result = await use_case.execute(login_request)

    # Assert
    assert isinstance(result, TokenResponse)
    assert result.access_token == sample_token.access_token
    assert result.refresh_token == sample_token.refresh_token
    assert result.token_type == "bearer"

    mock_service.login.assert_called_once_with(
        login_request.email,
        login_request.password,
    )


@pytest.mark.asyncio
async def test_login_with_different_credentials(mock_service):
    """Test login with different email/password combinations."""
    # Arrange
    login_data = LoginRequest(
        email="alice@example.com",
        password="AnotherPass456!",
    )

    token = Token(
        access_token="different_access_token_xyz",
        refresh_token="different_refresh_token_xyz",
    )

    mock_service.login = AsyncMock(return_value=token)
    use_case = LoginUseCase(mock_service)

    # Act
    result = await use_case.execute(login_data)

    # Assert
    assert result.access_token == token.access_token
    assert result.refresh_token == token.refresh_token

    mock_service.login.assert_called_once_with(
        "alice@example.com",
        "AnotherPass456!",
    )


@pytest.mark.asyncio
async def test_login_response_has_bearer_token_type(
    mock_service, login_request, sample_token
):
    """Test that login response includes default token_type."""
    # Arrange
    mock_service.login = AsyncMock(return_value=sample_token)
    use_case = LoginUseCase(mock_service)

    # Act
    result = await use_case.execute(login_request)

    # Assert
    assert hasattr(result, "token_type")
    assert result.token_type == "bearer"


@pytest.mark.asyncio
async def test_login_response_structure(mock_service, login_request, sample_token):
    """Test that login response has all expected fields."""
    # Arrange
    mock_service.login = AsyncMock(return_value=sample_token)
    use_case = LoginUseCase(mock_service)

    # Act
    result = await use_case.execute(login_request)

    # Assert
    assert hasattr(result, "access_token")
    assert hasattr(result, "refresh_token")
    assert hasattr(result, "token_type")
    assert len(result.access_token) > 0
    assert len(result.refresh_token) > 0


@pytest.mark.asyncio
async def test_login_service_called_with_exact_credentials(
    mock_service, login_request, sample_token
):
    """Test that service.login is called with exact email and password."""
    # Arrange
    mock_service.login = AsyncMock(return_value=sample_token)
    use_case = LoginUseCase(mock_service)

    # Act
    await use_case.execute(login_request)

    # Assert
    mock_service.login.assert_called_once()
    call_args = mock_service.login.call_args[0]
    assert call_args[0] == login_request.email
    assert call_args[1] == login_request.password


@pytest.mark.asyncio
async def test_login_converts_token_to_response(
    mock_service, login_request, sample_token
):
    """Test that Token entity is converted to TokenResponse schema."""
    # Arrange
    mock_service.login = AsyncMock(return_value=sample_token)
    use_case = LoginUseCase(mock_service)

    # Act
    result = await use_case.execute(login_request)

    # Assert
    assert type(result).__name__ == "TokenResponse"
    assert result.access_token == sample_token.access_token
    assert result.refresh_token == sample_token.refresh_token
