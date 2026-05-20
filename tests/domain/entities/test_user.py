"""Unit tests for User entity."""

import uuid
from datetime import datetime

import pytest

from app.domain.entities.user import User, UserRole, UserStatus


@pytest.fixture
def sample_user_data():
    """Create sample user data for testing."""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "hashed_password": "$2b$12$hashed_password_example",
        "full_name": "Test User",
        "role": UserRole.USER,
        "status": UserStatus.ACTIVE,
        "is_verified": False,
    }


@pytest.mark.asyncio
async def test_user_creation_with_all_fields(sample_user_data):
    """Test that User can be created with all fields."""
    user = User(**sample_user_data)

    assert user.email == sample_user_data["email"]
    assert user.username == sample_user_data["username"]
    assert user.hashed_password == sample_user_data["hashed_password"]
    assert user.full_name == sample_user_data["full_name"]
    assert user.role == UserRole.USER
    assert user.status == UserStatus.ACTIVE
    assert user.is_verified is False


@pytest.mark.asyncio
async def test_user_id_auto_generated():
    """Test that user ID is auto-generated as UUID."""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_pass",
    )

    assert user.id is not None
    assert isinstance(user.id, uuid.UUID)


@pytest.mark.asyncio
async def test_user_with_custom_id():
    """Test that user can be created with custom ID."""
    custom_id = uuid.uuid4()
    user = User(
        id=custom_id,
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_pass",
    )

    assert user.id == custom_id


@pytest.mark.asyncio
async def test_user_role_defaults_to_user():
    """Test that user role defaults to USER."""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_pass",
    )

    assert user.role == UserRole.USER


@pytest.mark.asyncio
async def test_user_status_defaults_to_active():
    """Test that user status defaults to ACTIVE."""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_pass",
    )

    assert user.status == UserStatus.ACTIVE


@pytest.mark.asyncio
async def test_user_is_verified_defaults_to_false():
    """Test that is_verified defaults to False."""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_pass",
    )

    assert user.is_verified is False


@pytest.mark.asyncio
async def test_user_full_name_is_optional():
    """Test that full_name is optional."""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_pass",
    )

    assert user.full_name is None


@pytest.mark.asyncio
async def test_user_created_at_auto_generated():
    """Test that created_at is auto-generated."""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_pass",
    )

    assert user.created_at is not None
    assert isinstance(user.created_at, datetime)


@pytest.mark.asyncio
async def test_user_updated_at_auto_generated():
    """Test that updated_at is auto-generated."""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_pass",
    )

    assert user.updated_at is not None
    assert isinstance(user.updated_at, datetime)


@pytest.mark.asyncio
async def test_user_with_all_roles():
    """Test User with all valid roles."""
    for role in UserRole:
        user = User(
            email=f"{role.value}@example.com",
            username=f"{role.value}user",
            hashed_password="hashed_pass",
            role=role,
        )

        assert user.role == role


@pytest.mark.asyncio
async def test_user_with_all_statuses():
    """Test User with all valid statuses."""
    for status in UserStatus:
        user = User(
            email=f"test{status.value}@example.com",
            username=f"user_{status.value}",
            hashed_password="hashed_pass",
            status=status,
        )

        assert user.status == status


@pytest.mark.asyncio
async def test_user_username_lowercased():
    """Test that username is lowercased."""
    user = User(
        email="test@example.com",
        username="TestUser",
        hashed_password="hashed_pass",
    )

    assert user.username == "testuser"


@pytest.mark.asyncio
async def test_user_username_with_underscores_allowed():
    """Test that username with underscores is valid."""
    user = User(
        email="test@example.com",
        username="Test_User_123",
        hashed_password="hashed_pass",
    )

    assert "test_user_123" == user.username


@pytest.mark.asyncio
async def test_user_username_with_hyphens_allowed():
    """Test that username with hyphens is valid."""
    user = User(
        email="test@example.com",
        username="Test-User-123",
        hashed_password="hashed_pass",
    )

    assert "test-user-123" == user.username


@pytest.mark.asyncio
async def test_user_username_rejects_special_characters():
    """Test that username rejects non-alphanumeric characters."""
    with pytest.raises(ValueError):
        User(
            email="test@example.com",
            username="Test@User!",
            hashed_password="hashed_pass",
        )


@pytest.mark.asyncio
async def test_user_username_minimum_length():
    """Test that username must be at least 3 characters."""
    with pytest.raises(ValueError):
        User(
            email="test@example.com",
            username="ab",
            hashed_password="hashed_pass",
        )


@pytest.mark.asyncio
async def test_user_username_maximum_length():
    """Test that username cannot exceed 50 characters."""
    with pytest.raises(ValueError):
        User(
            email="test@example.com",
            username="a" * 51,
            hashed_password="hashed_pass",
        )


@pytest.mark.asyncio
async def test_user_is_active_property_true():
    """Test is_active property returns True for ACTIVE status."""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_pass",
        status=UserStatus.ACTIVE,
    )

    assert user.is_active is True


@pytest.mark.asyncio
async def test_user_is_active_property_false():
    """Test is_active property returns False for non-ACTIVE status."""
    for status in [UserStatus.INACTIVE, UserStatus.BANNED]:
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_pass",
            status=status,
        )

        assert user.is_active is False


@pytest.mark.asyncio
async def test_user_is_admin_property_true():
    """Test is_admin property returns True for ADMIN role."""
    user = User(
        email="admin@example.com",
        username="adminuser",
        hashed_password="hashed_pass",
        role=UserRole.ADMIN,
    )

    assert user.is_admin is True


@pytest.mark.asyncio
async def test_user_is_admin_property_false():
    """Test is_admin property returns False for non-ADMIN role."""
    for role in [UserRole.USER, UserRole.MODERATOR]:
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_pass",
            role=role,
        )

        assert user.is_admin is False


@pytest.mark.asyncio
async def test_user_has_role_method_single_role():
    """Test has_role method with single role."""
    user = User(
        email="admin@example.com",
        username="adminuser",
        hashed_password="hashed_pass",
        role=UserRole.ADMIN,
    )

    assert user.has_role(UserRole.ADMIN) is True
    assert user.has_role(UserRole.USER) is False


@pytest.mark.asyncio
async def test_user_has_role_method_multiple_roles():
    """Test has_role method with multiple roles."""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_pass",
        role=UserRole.USER,
    )

    assert user.has_role(UserRole.USER, UserRole.ADMIN) is True
    assert user.has_role(UserRole.ADMIN, UserRole.MODERATOR) is False


@pytest.mark.asyncio
async def test_user_verified_flag():
    """Test user with is_verified flag set to True."""
    user = User(
        email="verified@example.com",
        username="verifieduser",
        hashed_password="hashed_pass",
        is_verified=True,
    )

    assert user.is_verified is True


@pytest.mark.asyncio
async def test_user_with_full_name():
    """Test user with full name."""
    full_name = "John Doe Smith"
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_pass",
        full_name=full_name,
    )

    assert user.full_name == full_name


@pytest.mark.asyncio
async def test_user_full_name_maximum_length():
    """Test that full_name cannot exceed 120 characters."""
    with pytest.raises(ValueError):
        User(
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_pass",
            full_name="a" * 121,
        )


@pytest.mark.asyncio
async def test_user_email_validation():
    """Test that user email is validated."""
    with pytest.raises(ValueError):
        User(
            email="not-a-valid-email",
            username="testuser",
            hashed_password="hashed_pass",
        )


@pytest.mark.asyncio
async def test_user_valid_email_formats():
    """Test user with various valid email formats."""
    valid_emails = [
        "test@example.com",
        "user.name@example.com",
        "user+tag@example.co.uk",
        "123@example.com",
    ]

    for email in valid_emails:
        user = User(
            email=email,
            username="testuser",
            hashed_password="hashed_pass",
        )

        assert user.email == email


@pytest.mark.asyncio
async def test_user_serialization_to_dict():
    """Test that User can be serialized to dictionary."""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_pass",
        full_name="Test User",
    )

    user_dict = user.model_dump()

    assert user_dict["email"] == "test@example.com"
    assert user_dict["username"] == "testuser"
    assert user_dict["hashed_password"] == "hashed_pass"
    assert user_dict["full_name"] == "Test User"


@pytest.mark.asyncio
async def test_user_model_copy():
    """Test that user can be copied with updates."""
    original = User(
        email="original@example.com",
        username="originaluser",
        hashed_password="hashed_pass",
        status=UserStatus.ACTIVE,
    )

    updated = original.model_copy(
        update={"status": UserStatus.INACTIVE, "is_verified": True}
    )

    assert original.status == UserStatus.ACTIVE
    assert original.is_verified is False
    assert updated.status == UserStatus.INACTIVE
    assert updated.is_verified is True
    assert updated.email == original.email
