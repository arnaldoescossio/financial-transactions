from unittest.mock import AsyncMock, Mock

import pytest

from app.domain.entities.account import AccountCreate, AccountResponse
from app.domain.repositories.account_repository import AccountRepository
from app.infrastructure.models.account_model import AccountModel
from app.use_cases.account.create_account import CreateAccountUseCase


@pytest.fixture
def mock_repository():
    """Create a mock account repository for testing."""
    return Mock(spec=AccountRepository)


@pytest.fixture
def create_account_data():
    """Create sample account data for testing."""
    return AccountCreate(balance=500.0, type="checking")


@pytest.fixture
def mock_account_model():
    """Create a mock persisted account model."""
    account = Mock(spec=AccountModel)
    account.id = 1
    account.balance = 500.0
    account.type = "checking"
    return account


@pytest.mark.asyncio
async def test_create_account_success(
    mock_repository, create_account_data, mock_account_model
):
    """Test successful account creation."""
    # Arrange
    mock_repository.save = AsyncMock(return_value=mock_account_model)
    use_case = CreateAccountUseCase(mock_repository)

    # Act
    result = await use_case.execute(create_account_data)

    # Assert
    assert isinstance(result, AccountResponse)
    assert result.id == 1
    assert result.balance == 500.0
    assert result.type == "checking"
    mock_repository.save.assert_called_once_with(create_account_data)


@pytest.mark.asyncio
async def test_create_account_with_savings_type(mock_repository):
    """Test successful account creation with savings account type."""
    # Arrange
    account_data = AccountCreate(balance=1200.0, type="savings")

    mock_account = Mock(spec=AccountModel)
    mock_account.id = 2
    mock_account.balance = 1200.0
    mock_account.type = "savings"

    mock_repository.save = AsyncMock(return_value=mock_account)
    use_case = CreateAccountUseCase(mock_repository)

    # Act
    result = await use_case.execute(account_data)

    # Assert
    assert result.id == 2
    assert result.balance == 1200.0
    assert result.type == "savings"
    mock_repository.save.assert_called_once_with(account_data)


@pytest.mark.asyncio
async def test_create_account_response_structure(
    mock_repository, create_account_data, mock_account_model
):
    """Test that account response has all expected fields."""
    # Arrange
    mock_repository.save = AsyncMock(return_value=mock_account_model)
    use_case = CreateAccountUseCase(mock_repository)

    # Act
    result = await use_case.execute(create_account_data)

    # Assert
    assert hasattr(result, "id")
    assert hasattr(result, "balance")
    assert hasattr(result, "type")
    assert hasattr(result, "transactions")


@pytest.mark.asyncio
async def test_create_account_repository_called_with_correct_data(
    mock_repository, create_account_data
):
    """Test that repository.save is called with the same account payload."""
    # Arrange
    mock_account = Mock(spec=AccountModel)
    mock_account.id = 3
    mock_account.balance = create_account_data.balance
    mock_account.type = create_account_data.type

    mock_repository.save = AsyncMock(return_value=mock_account)
    use_case = CreateAccountUseCase(mock_repository)

    # Act
    await use_case.execute(create_account_data)

    # Assert
    mock_repository.save.assert_called_once()
    saved_account = mock_repository.save.call_args[0][0]
    assert saved_account.balance == create_account_data.balance
    assert saved_account.type == create_account_data.type
