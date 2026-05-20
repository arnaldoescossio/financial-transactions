"""Unit tests for UserRepository."""

import uuid
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.domain.entities.user import User, UserRole, UserStatus
from app.infrastructure.adapters.repositories.user_repository import UserRepository
from app.infrastructure.models.user_model import UserModel


@pytest.fixture
def mock_db_session():
    """Create a mock database session."""
    session = MagicMock()
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.execute = AsyncMock()
    session.merge = AsyncMock()
    return session


@pytest.fixture
def repository(mock_db_session):
    """Create a UserRepository with mocked database session."""
    return UserRepository(mock_db_session)


@pytest.fixture
def sample_user_id():
    """Generate a sample UUID for testing."""
    return uuid.uuid4()


@pytest.fixture
def sample_user(sample_user_id):
    """Create a sample User entity for testing."""
    return User(
        id=sample_user_id,
        email="john@example.com",
        username="johndoe",
        hashed_password="$2b$12$hashed_password_example",
        full_name="John Doe",
        role=UserRole.USER,
        status=UserStatus.ACTIVE,
        is_verified=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


@pytest.fixture
def sample_user_model(sample_user_id):
    """Create a sample UserModel for testing."""
    model = MagicMock(spec=UserModel)
    model.id = sample_user_id
    model.email = "john@example.com"
    model.username = "johndoe"
    model.hashed_password = "$2b$12$hashed_password_example"
    model.full_name = "John Doe"
    model.role = UserRole.USER
    model.status = UserStatus.ACTIVE
    model.is_verified = True
    model.created_at = datetime.utcnow()
    model.updated_at = datetime.utcnow()
    return model


@pytest.mark.asyncio
async def test_get_by_id_returns_user(
    repository, mock_db_session, sample_user_model, sample_user_id
):
    """Test that get_by_id retrieves a user by ID."""
    result_mock = MagicMock()
    result_mock.scalars.return_value.first.return_value = sample_user_model
    mock_db_session.execute = AsyncMock(return_value=result_mock)

    result = await repository.get_by_id(sample_user_id)

    assert isinstance(result, User)
    assert result.id == sample_user_id
    assert result.email == "john@example.com"
    assert result.username == "johndoe"
    assert result.role == UserRole.USER
    assert result.status == UserStatus.ACTIVE
    mock_db_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_by_id_returns_none_when_not_found(repository, mock_db_session):
    """Test that get_by_id returns None when user is not found."""
    result_mock = MagicMock()
    result_mock.scalars.return_value.first.return_value = None
    mock_db_session.execute = AsyncMock(return_value=result_mock)

    result = await repository.get_by_id(uuid.uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_get_by_email_returns_user(
    repository, mock_db_session, sample_user_model
):
    """Test that get_by_email retrieves a user by email."""
    result_mock = MagicMock()
    result_mock.scalars.return_value.first.return_value = sample_user_model
    mock_db_session.execute = AsyncMock(return_value=result_mock)

    result = await repository.get_by_email("john@example.com")

    assert isinstance(result, User)
    assert result.email == "john@example.com"
    mock_db_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_by_email_returns_none_when_not_found(repository, mock_db_session):
    """Test that get_by_email returns None when user is not found."""
    result_mock = MagicMock()
    result_mock.scalars.return_value.first.return_value = None
    mock_db_session.execute = AsyncMock(return_value=result_mock)

    result = await repository.get_by_email("nonexistent@example.com")

    assert result is None


@pytest.mark.asyncio
async def test_get_by_username_returns_user(
    repository, mock_db_session, sample_user_model
):
    """Test that get_by_username retrieves a user by username."""
    result_mock = MagicMock()
    result_mock.scalars.return_value.first.return_value = sample_user_model
    mock_db_session.execute = AsyncMock(return_value=result_mock)

    result = await repository.get_by_username("johndoe")

    assert isinstance(result, User)
    assert result.username == "johndoe"
    mock_db_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_by_username_returns_none_when_not_found(repository, mock_db_session):
    """Test that get_by_username returns None when user is not found."""
    result_mock = MagicMock()
    result_mock.scalars.return_value.first.return_value = None
    mock_db_session.execute = AsyncMock(return_value=result_mock)

    result = await repository.get_by_username("nonexistent_user")

    assert result is None


@pytest.mark.asyncio
async def test_create_persists_user_and_refreshes(
    repository, mock_db_session, sample_user
):
    """Test that create persists a user and refreshes the model."""
    result = await repository.create(sample_user)

    assert isinstance(result, User)
    assert result.email == sample_user.email
    assert result.username == sample_user.username

    mock_db_session.add.assert_called_once()
    added_model = mock_db_session.add.call_args[0][0]
    assert isinstance(added_model, UserModel)
    assert added_model.email == sample_user.email
    assert added_model.username == sample_user.username
    assert added_model.role == sample_user.role

    mock_db_session.commit.assert_awaited_once()
    mock_db_session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_with_admin_role(repository, mock_db_session, sample_user):
    """Test that create handles different user roles correctly."""
    admin_user = sample_user.model_copy(update={"role": UserRole.ADMIN})

    await repository.create(admin_user)

    added_model = mock_db_session.add.call_args[0][0]
    assert added_model.role == UserRole.ADMIN


@pytest.mark.asyncio
async def test_update_merges_user_and_refreshes(
    repository, mock_db_session, sample_user
):
    """Test that update merges user changes and refreshes the model."""
    updated_user = sample_user.model_copy(
        update={"full_name": "John Doe Updated", "status": UserStatus.INACTIVE}
    )

    result = await repository.update(updated_user)

    assert isinstance(result, User)
    assert result.full_name == "John Doe Updated"
    assert result.status == UserStatus.INACTIVE

    mock_db_session.merge.assert_awaited_once()
    merged_model = mock_db_session.merge.call_args[0][0]
    assert isinstance(merged_model, UserModel)
    assert merged_model.full_name == "John Doe Updated"

    mock_db_session.commit.assert_awaited_once()
    mock_db_session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_removes_user(repository, mock_db_session, sample_user_id):
    """Test that delete removes a user by ID."""
    await repository.delete(sample_user_id)

    mock_db_session.execute.assert_awaited_once()
    mock_db_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_exists_by_email_returns_true(repository, mock_db_session):
    """Test that exists_by_email returns True when user exists."""
    result_mock = MagicMock()
    result_mock.scalar_one.return_value = 1
    mock_db_session.execute = AsyncMock(return_value=result_mock)

    exists = await repository.exists_by_email("john@example.com")

    assert exists is True
    mock_db_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_exists_by_email_returns_false(repository, mock_db_session):
    """Test that exists_by_email returns False when user does not exist."""
    result_mock = MagicMock()
    result_mock.scalar_one.return_value = 0
    mock_db_session.execute = AsyncMock(return_value=result_mock)

    exists = await repository.exists_by_email("nonexistent@example.com")

    assert exists is False


@pytest.mark.asyncio
async def test_to_domain_converts_model_to_entity(sample_user_model):
    """Test that _to_domain converts a UserModel to User entity."""
    user = UserRepository._to_domain(sample_user_model)

    assert isinstance(user, User)
    assert user.email == sample_user_model.email
    assert user.username == sample_user_model.username


@pytest.mark.asyncio
async def test_to_domain_returns_none_for_none_model():
    """Test that _to_domain returns None when given None."""
    user = UserRepository._to_domain(None)

    assert user is None


@pytest.mark.asyncio
async def test_to_model_converts_entity_to_model(sample_user):
    """Test that _to_model converts a User entity to UserModel."""
    model = UserRepository._to_model(sample_user)

    assert isinstance(model, UserModel)
    assert model.id == sample_user.id
    assert model.email == sample_user.email
    assert model.username == sample_user.username
    assert model.hashed_password == sample_user.hashed_password
    assert model.full_name == sample_user.full_name
    assert model.role == sample_user.role
    assert model.status == sample_user.status
    assert model.is_verified == sample_user.is_verified


@pytest.mark.asyncio
async def test_to_model_preserves_all_user_fields(sample_user):
    """Test that _to_model preserves all user entity fields."""
    model = UserRepository._to_model(sample_user)

    assert model.created_at == sample_user.created_at
    assert model.updated_at == sample_user.updated_at
    assert model.is_verified == sample_user.is_verified
