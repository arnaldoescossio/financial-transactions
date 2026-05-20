"""Unit tests for AuthService."""

import uuid
from unittest.mock import AsyncMock, Mock, patch

import pytest

from app.core.exceptions.auth_exceptions import CredentialsException
from app.core.exceptions.user_exceptions import InactiveUserException
from app.domain.entities.token import Token
from app.domain.entities.user import User, UserRole, UserStatus
from app.domain.service.auth_service import AuthService


@pytest.fixture
def mock_user_repo():
    """Create a mock user repository for testing."""
    return Mock()


@pytest.fixture
def auth_service(mock_user_repo):
    """Create an AuthService with mocked repository."""
    return AuthService(mock_user_repo)


@pytest.fixture
def sample_user():
    """Create a sample user entity for testing."""
    return User(
        id=uuid.uuid4(),
        email="test@example.com",
        username="testuser",
        hashed_password="$2b$12$hashed_password",
        full_name="Test User",
        role=UserRole.USER,
        status=UserStatus.ACTIVE,
        is_verified=False,
    )


@pytest.mark.asyncio
async def test_register_creates_user_with_hashed_password(
    auth_service, mock_user_repo, sample_user
):
    """Test that register creates a user with hashed password."""
    mock_user_repo.create = AsyncMock(return_value=sample_user)
    auth_service._users = mock_user_repo

    result = await auth_service.register(
        email="test@example.com",
        username="testuser",
        password="PlainPass123!",
        full_name="Test User",
    )

    assert isinstance(result, User)
    assert result.email == "test@example.com"
    assert result.username == "testuser"
    mock_user_repo.create.assert_awaited_once()


@pytest.mark.asyncio
async def test_register_hashes_password_before_storage(auth_service, mock_user_repo):
    """Test that register hashes the password."""
    created_user = User(
        id=uuid.uuid4(),
        email="newuser@example.com",
        username="newuser",
        hashed_password="$2b$12$hashed",
        full_name="New User",
    )
    mock_user_repo.create = AsyncMock(return_value=created_user)
    auth_service._users = mock_user_repo

    await auth_service.register(
        email="newuser@example.com",
        username="newuser",
        password="SecurePass456!",
        full_name="New User",
    )

    # Verify that the created user has a hashed password, not the plaintext
    called_user = mock_user_repo.create.call_args[0][0]
    assert called_user.hashed_password != "SecurePass456!"
    assert called_user.hashed_password.startswith(("$2a$", "$2b$", "$2y$"))


@pytest.mark.asyncio
async def test_register_with_default_role(auth_service, mock_user_repo):
    """Test that register defaults to USER role."""
    created_user = User(
        id=uuid.uuid4(),
        email="user@example.com",
        username="user",
        hashed_password="$2b$12$hashed",
        role=UserRole.USER,
    )
    mock_user_repo.create = AsyncMock(return_value=created_user)
    auth_service._users = mock_user_repo

    result = await auth_service.register(
        email="user@example.com",
        username="user",
        password="Pass123!",
    )

    assert result.role == UserRole.USER
    called_user = mock_user_repo.create.call_args[0][0]
    assert called_user.role == UserRole.USER


@pytest.mark.asyncio
async def test_register_with_admin_role(auth_service, mock_user_repo):
    """Test that register can create admin users."""
    created_user = User(
        id=uuid.uuid4(),
        email="admin@example.com",
        username="admin",
        hashed_password="$2b$12$hashed",
        role=UserRole.ADMIN,
    )
    mock_user_repo.create = AsyncMock(return_value=created_user)
    auth_service._users = mock_user_repo

    result = await auth_service.register(
        email="admin@example.com",
        username="admin",
        password="AdminPass123!",
        role=UserRole.ADMIN,
    )

    assert result.role == UserRole.ADMIN


@pytest.mark.asyncio
async def test_register_without_full_name(auth_service, mock_user_repo):
    """Test that register works without full_name."""
    created_user = User(
        id=uuid.uuid4(),
        email="user@example.com",
        username="user",
        hashed_password="$2b$12$hashed",
        full_name=None,
    )
    mock_user_repo.create = AsyncMock(return_value=created_user)
    auth_service._users = mock_user_repo

    result = await auth_service.register(
        email="user@example.com",
        username="user",
        password="Pass123!",
    )

    assert result.full_name is None


@pytest.mark.asyncio
async def test_get_by_email_returns_user(auth_service, mock_user_repo, sample_user):
    """Test that get_by_email returns the user."""
    mock_user_repo.get_by_email = AsyncMock(return_value=sample_user)
    auth_service._users = mock_user_repo

    result = await auth_service.get_by_email("test@example.com")

    assert isinstance(result, User)
    assert result.email == "test@example.com"
    mock_user_repo.get_by_email.assert_awaited_once_with("test@example.com")


@pytest.mark.asyncio
async def test_get_by_email_returns_none_when_not_found(auth_service, mock_user_repo):
    """Test that get_by_email returns None when user not found."""
    mock_user_repo.get_by_email = AsyncMock(return_value=None)
    auth_service._users = mock_user_repo

    result = await auth_service.get_by_email("nonexistent@example.com")

    assert result is None


@pytest.mark.asyncio
async def test_get_by_username_returns_user(auth_service, mock_user_repo, sample_user):
    """Test that get_by_username returns the user."""
    mock_user_repo.get_by_username = AsyncMock(return_value=sample_user)
    auth_service._users = mock_user_repo

    result = await auth_service.get_by_username("testuser")

    assert isinstance(result, User)
    assert result.username == "testuser"
    mock_user_repo.get_by_username.assert_awaited_once_with("testuser")


@pytest.mark.asyncio
async def test_get_by_username_returns_none_when_not_found(
    auth_service, mock_user_repo
):
    """Test that get_by_username returns None when user not found."""
    mock_user_repo.get_by_username = AsyncMock(return_value=None)
    auth_service._users = mock_user_repo

    result = await auth_service.get_by_username("nonexistentuser")

    assert result is None


@pytest.mark.asyncio
async def test_login_success(auth_service, mock_user_repo, sample_user):
    """Test successful login returns token."""
    mock_user_repo.get_by_email = AsyncMock(return_value=sample_user)
    auth_service._users = mock_user_repo

    with patch("app.domain.service.auth_service.verify_password") as mock_verify:
        with patch("app.domain.service.auth_service.jwt_service") as mock_jwt:
            mock_verify.return_value = True
            mock_jwt.create_access_token.return_value = ("access_token_xyz", "jti_1")
            mock_jwt.create_refresh_token.return_value = ("refresh_token_xyz", "jti_2")

            result = await auth_service.login("test@example.com", "PlainPass123!")

            assert isinstance(result, Token)
            assert result.access_token == "access_token_xyz"
            assert result.refresh_token == "refresh_token_xyz"


@pytest.mark.asyncio
async def test_login_fails_with_invalid_email(auth_service, mock_user_repo):
    """Test login fails when email not found."""
    mock_user_repo.get_by_email = AsyncMock(return_value=None)
    auth_service._users = mock_user_repo

    with pytest.raises(CredentialsException) as exc_info:
        await auth_service.login("nonexistent@example.com", "Password123!")

    assert "Invalid email or password" in str(exc_info.value)


@pytest.mark.asyncio
async def test_login_fails_with_wrong_password(
    auth_service, mock_user_repo, sample_user
):
    """Test login fails when password is incorrect."""
    mock_user_repo.get_by_email = AsyncMock(return_value=sample_user)
    auth_service._users = mock_user_repo

    with patch("app.domain.service.auth_service.verify_password") as mock_verify:
        mock_verify.return_value = False

        with pytest.raises(CredentialsException) as exc_info:
            await auth_service.login("test@example.com", "WrongPassword123!")

        assert "Invalid email or password" in str(exc_info.value)


@pytest.mark.asyncio
async def test_login_fails_with_inactive_user(auth_service, mock_user_repo):
    """Test login fails when user is inactive."""
    inactive_user = User(
        id=uuid.uuid4(),
        email="inactive@example.com",
        username="inactiveuser",
        hashed_password="$2b$12$hashed",
        status=UserStatus.INACTIVE,
    )
    mock_user_repo.get_by_email = AsyncMock(return_value=inactive_user)
    auth_service._users = mock_user_repo

    with patch("app.domain.service.auth_service.verify_password") as mock_verify:
        mock_verify.return_value = True

        with pytest.raises(InactiveUserException):
            await auth_service.login("inactive@example.com", "Pass123!")


@pytest.mark.asyncio
async def test_login_fails_with_banned_user(auth_service, mock_user_repo):
    """Test login fails when user is banned."""
    banned_user = User(
        id=uuid.uuid4(),
        email="banned@example.com",
        username="banneduser",
        hashed_password="$2b$12$hashed",
        status=UserStatus.BANNED,
    )
    mock_user_repo.get_by_email = AsyncMock(return_value=banned_user)
    auth_service._users = mock_user_repo

    with patch("app.domain.service.auth_service.verify_password") as mock_verify:
        mock_verify.return_value = True

        with pytest.raises(InactiveUserException):
            await auth_service.login("banned@example.com", "Pass123!")


@pytest.mark.asyncio
async def test_login_calls_verify_password_with_correct_arguments(
    auth_service, mock_user_repo, sample_user
):
    """Test that login calls verify_password with correct arguments."""
    mock_user_repo.get_by_email = AsyncMock(return_value=sample_user)
    auth_service._users = mock_user_repo

    with patch("app.domain.service.auth_service.verify_password") as mock_verify_password:
        with patch("app.domain.service.auth_service.jwt_service")as mock_jwt_service:
            mock_verify_password.return_value = True
            mock_jwt_service.create_access_token.return_value = ("access", "jti_1")
            mock_jwt_service.create_refresh_token.return_value = ("refresh", "jti_2")

            await auth_service.login("test@example.com", "PlainPass123!")

            mock_verify_password.assert_called_once_with(
                "PlainPass123!", sample_user.hashed_password
            )


@pytest.mark.asyncio
async def test_login_calls_jwt_service_with_correct_arguments(
    auth_service, mock_user_repo, sample_user
):
    """Test that login calls jwt_service with user ID and role."""
    mock_user_repo.get_by_email = AsyncMock(return_value=sample_user)
    auth_service._users = mock_user_repo

    with patch("app.domain.service.auth_service.verify_password") as mock_verify_password:
        with patch("app.domain.service.auth_service.jwt_service") as mock_jwt_service:
            mock_verify_password.return_value = True
            mock_jwt_service.create_access_token.return_value = ("access", "jti_1")
            mock_jwt_service.create_refresh_token.return_value = ("refresh", "jti_2")

            await auth_service.login("test@example.com", "PlainPass123!")

            mock_jwt_service.create_access_token.assert_called_once_with(
                str(sample_user.id), sample_user.role
            )
            mock_jwt_service.create_refresh_token.assert_called_once_with(str(sample_user.id))


@pytest.mark.asyncio
async def test_register_delegates_to_repository(auth_service, mock_user_repo):
    """Test that register delegates user creation to repository."""
    created_user = User(
        id=uuid.uuid4(),
        email="newuser@example.com",
        username="newuser",
        hashed_password="$2b$12$hashed",
    )
    mock_user_repo.create = AsyncMock(return_value=created_user)
    auth_service._users = mock_user_repo

    result = await auth_service.register(
        email="newuser@example.com",
        username="newuser",
        password="Pass123!",
    )

    assert result.id == created_user.id
    mock_user_repo.create.assert_awaited_once()


@pytest.mark.asyncio
async def test_multiple_logins_different_users(auth_service, mock_user_repo):
    """Test login for multiple different users."""
    user1 = User(
        id=uuid.uuid4(),
        email="user1@example.com",
        username="user1",
        hashed_password="$2b$12$hash1",
        status=UserStatus.ACTIVE,
    )
    user2 = User(
        id=uuid.uuid4(),
        email="user2@example.com",
        username="user2",
        hashed_password="$2b$12$hash2",
        status=UserStatus.ACTIVE,
    )

    with patch("app.domain.service.auth_service.verify_password") as mock_verify:
        with patch("app.domain.service.auth_service.jwt_service") as mock_jwt:
            mock_verify.return_value = True
            mock_jwt.create_access_token.return_value = ("access", "jti")
            mock_jwt.create_refresh_token.return_value = ("refresh", "jti")

            mock_user_repo.get_by_email = AsyncMock(side_effect=[user1, user2])
            auth_service._users = mock_user_repo

            result1 = await auth_service.login("user1@example.com", "pass1")
            result2 = await auth_service.login("user2@example.com", "pass2")

            assert isinstance(result1, Token)
            assert isinstance(result2, Token)
            assert mock_user_repo.get_by_email.await_count == 2
