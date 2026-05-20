"""Unit tests for RegisterUserUseCase."""

import uuid
from datetime import datetime
from unittest.mock import AsyncMock, Mock

import pytest

from app.api.v1.schemas.auth_schema import RegisterRequest
from app.api.v1.schemas.user_schema import UserResponse
from app.core.exceptions.user_exceptions import UserAlreadyExistsException
from app.domain.entities.user import User, UserRole, UserStatus
from app.domain.service.auth_service import AuthService
from app.use_cases.authentication.register_user import RegisterUserUseCase


@pytest.fixture
def mock_service():
    """Create a mock auth service for testing."""
    return Mock(spec=AuthService)


@pytest.fixture
def register_request():
    """Create sample registration request data for testing."""
    return RegisterRequest(
        email="newuser@example.com",
        username="newuser",
        password="SecurePass123!",
        full_name="New User",
    )


@pytest.fixture
def register_request_no_full_name():
    """Create registration request without full_name."""
    return RegisterRequest(
        email="another@example.com",
        username="anotheruser",
        password="AnotherPass456!",
    )


@pytest.fixture
def sample_user():
    """Create a sample user entity for testing."""
    return User(
        id=uuid.uuid4(),
        email="newuser@example.com",
        username="newuser",
        hashed_password="$2b$12$hashed_password_example",
        full_name="New User",
        role=UserRole.USER,
        status=UserStatus.ACTIVE,
        is_verified=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


@pytest.mark.asyncio
async def test_register_user_success(mock_service, register_request, sample_user):
    """Test successful user registration returns UserResponse."""
    # Arrange
    mock_service.get_by_email = AsyncMock(return_value=None)
    mock_service.get_by_username = AsyncMock(return_value=None)
    mock_service.register = AsyncMock(return_value=sample_user)
    use_case = RegisterUserUseCase(mock_service)

    # Act
    result = await use_case.execute(register_request)

    # Assert
    assert isinstance(result, UserResponse)
    assert result.email == sample_user.email
    assert result.username == sample_user.username
    assert result.full_name == sample_user.full_name
    assert result.role == UserRole.USER
    assert result.status == UserStatus.ACTIVE

    mock_service.get_by_email.assert_called_once_with(register_request.email)
    mock_service.get_by_username.assert_called_once_with(register_request.username)
    mock_service.register.assert_called_once_with(
        email=register_request.email,
        username=register_request.username,
        password=register_request.password,
        full_name=register_request.full_name,
    )


@pytest.mark.asyncio
async def test_register_user_without_full_name(
    mock_service, register_request_no_full_name, sample_user
):
    """Test registration without full_name field."""
    # Arrange
    mock_service.get_by_email = AsyncMock(return_value=None)
    mock_service.get_by_username = AsyncMock(return_value=None)

    user_without_full_name = sample_user.model_copy(update={"full_name": None})
    mock_service.register = AsyncMock(return_value=user_without_full_name)
    use_case = RegisterUserUseCase(mock_service)

    # Act
    result = await use_case.execute(register_request_no_full_name)

    # Assert
    assert result.full_name is None
    mock_service.register.assert_called_once_with(
        email=register_request_no_full_name.email,
        username=register_request_no_full_name.username,
        password=register_request_no_full_name.password,
        full_name=None,
    )


@pytest.mark.asyncio
async def test_register_user_email_already_exists(mock_service, register_request):
    """Test registration fails when email already exists."""
    # Arrange
    existing_user = Mock(spec=User)
    existing_user.email = register_request.email
    mock_service.get_by_email = AsyncMock(return_value=existing_user)
    use_case = RegisterUserUseCase(mock_service)

    # Act & Assert
    with pytest.raises(UserAlreadyExistsException):
        await use_case.execute(register_request)

    mock_service.get_by_email.assert_called_once_with(register_request.email)
    mock_service.get_by_username.assert_not_called()
    mock_service.register.assert_not_called()


@pytest.mark.asyncio
async def test_register_user_username_already_exists(mock_service, register_request):
    """Test registration fails when username already exists."""
    # Arrange
    existing_user = Mock(spec=User)
    existing_user.username = register_request.username
    mock_service.get_by_email = AsyncMock(return_value=None)
    mock_service.get_by_username = AsyncMock(return_value=existing_user)
    use_case = RegisterUserUseCase(mock_service)

    # Act & Assert
    with pytest.raises(UserAlreadyExistsException):
        await use_case.execute(register_request)

    mock_service.get_by_email.assert_called_once_with(register_request.email)
    mock_service.get_by_username.assert_called_once_with(register_request.username)
    mock_service.register.assert_not_called()


@pytest.mark.asyncio
async def test_register_user_response_structure(
    mock_service, register_request, sample_user
):
    """Test that registration response has all expected fields."""
    # Arrange
    mock_service.get_by_email = AsyncMock(return_value=None)
    mock_service.get_by_username = AsyncMock(return_value=None)
    mock_service.register = AsyncMock(return_value=sample_user)
    use_case = RegisterUserUseCase(mock_service)

    # Act
    result = await use_case.execute(register_request)

    # Assert
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
async def test_register_user_checks_email_first(
    mock_service, register_request, sample_user
):
    """Test that email is checked before username."""
    # Arrange
    mock_service.get_by_email = AsyncMock(return_value=None)
    mock_service.get_by_username = AsyncMock(return_value=None)
    mock_service.register = AsyncMock(return_value=sample_user)
    use_case = RegisterUserUseCase(mock_service)

    # Act
    await use_case.execute(register_request)

    # Assert - verify email check was called before username check
    assert mock_service.get_by_email.call_count == 1
    assert mock_service.get_by_username.call_count == 1

    email_call_order = mock_service.get_by_email.call_args_list[0]
    username_call_order = mock_service.get_by_username.call_args_list[0]
    assert email_call_order[0][0] == register_request.email
    assert username_call_order[0][0] == register_request.username


@pytest.mark.asyncio
async def test_register_user_with_different_credentials(mock_service):
    """Test registration with different email and username."""
    # Arrange
    different_request = RegisterRequest(
        email="alice@example.com",
        username="alice_smith",
        password="AlicePass789!",
        full_name="Alice Smith",
    )

    created_user = User(
        id=uuid.uuid4(),
        email=different_request.email,
        username=different_request.username,
        hashed_password="$2b$12$hashed_alice",
        full_name=different_request.full_name,
        role=UserRole.USER,
        status=UserStatus.ACTIVE,
        is_verified=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    mock_service.get_by_email = AsyncMock(return_value=None)
    mock_service.get_by_username = AsyncMock(return_value=None)
    mock_service.register = AsyncMock(return_value=created_user)
    use_case = RegisterUserUseCase(mock_service)

    # Act
    result = await use_case.execute(different_request)

    # Assert
    assert result.email == "alice@example.com"
    assert result.username == "alice_smith"
    assert result.full_name == "Alice Smith"

    mock_service.register.assert_called_once_with(
        email="alice@example.com",
        username="alice_smith",
        password="AlicePass789!",
        full_name="Alice Smith",
    )


@pytest.mark.asyncio
async def test_register_user_converts_user_to_response(
    mock_service, register_request, sample_user
):
    """Test that User entity is converted to UserResponse schema."""
    # Arrange
    mock_service.get_by_email = AsyncMock(return_value=None)
    mock_service.get_by_username = AsyncMock(return_value=None)
    mock_service.register = AsyncMock(return_value=sample_user)
    use_case = RegisterUserUseCase(mock_service)

    # Act
    result = await use_case.execute(register_request)

    # Assert
    assert type(result).__name__ == "UserResponse"
    assert result.id == sample_user.id
    assert result.email == sample_user.email
    assert result.username == sample_user.username
    assert result.is_verified == sample_user.is_verified
