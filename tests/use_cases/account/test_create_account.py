from unittest.mock import AsyncMock, Mock

import pytest

from app.api.v1.schemas.account_schema import AccountCreate, AccountResponse
from app.domain.entities.account import Account
from app.domain.service.account_service import AccountService
from app.use_cases.account.create_account import CreateAccountUseCase


@pytest.fixture
def mock_service():
    """Create a mock account service for testing."""
    return Mock(spec=AccountService)


@pytest.fixture
def create_account_data():
    """Create sample account data for testing."""
    return AccountCreate(balance=500.0, type="checking")


@pytest.fixture
def mock_account():
    """Create a mock persisted account model."""
    account = Mock(spec=Account)
    account.id = 1
    account.balance = 500.0
    account.type = "checking"
    account.transactions = []
    return account


@pytest.mark.asyncio
async def test_create_account_success(mock_service, create_account_data, mock_account):
    """Test successful account creation."""
    # Arrange
    mock_service.save = AsyncMock(return_value=mock_account)
    use_case = CreateAccountUseCase(mock_service)

    # Act
    result = await use_case.execute(create_account_data)

    # Assert
    assert isinstance(result, AccountResponse)
    assert result.id == 1
    assert result.balance == 500.0
    assert result.type == "checking"

    created_account = mock_service.save.call_args[0][0]
    mock_service.save.assert_called_once_with(created_account)


@pytest.mark.asyncio
async def test_create_account_with_savings_type(mock_service):
    """Test successful account creation with savings account type."""
    # Arrange
    account_data = AccountCreate(balance=1200.0, type="savings")

    mock_account = Mock(spec=Account)
    mock_account.id = 2
    mock_account.balance = 1200.0
    mock_account.type = "savings"
    mock_account.transactions = []

    mock_service.save = AsyncMock(return_value=mock_account)
    use_case = CreateAccountUseCase(mock_service)

    # Act
    result = await use_case.execute(account_data)

    # Assert
    assert result.id == 2
    assert result.balance == 1200.0
    assert result.type == "savings"

    created_account = mock_service.save.call_args[0][0]
    mock_service.save.assert_called_once_with(created_account)


@pytest.mark.asyncio
async def test_create_account_response_structure(
    mock_service, create_account_data, mock_account
):
    """Test that account response has all expected fields."""
    # Arrange
    mock_service.save = AsyncMock(return_value=mock_account)
    use_case = CreateAccountUseCase(mock_service)

    # Act
    result = await use_case.execute(create_account_data)

    # Assert
    assert hasattr(result, "id")
    assert hasattr(result, "balance")
    assert hasattr(result, "type")
    assert hasattr(result, "transactions")


@pytest.mark.asyncio
async def test_create_account_repository_called_with_correct_data(
    mock_service, create_account_data
):
    """Test that repository.save is called with the same account payload."""
    # Arrange
    mock_account = Mock(spec=Account)
    mock_account.id = 3
    mock_account.balance = create_account_data.balance
    mock_account.type = create_account_data.type
    mock_account.transactions = []
    
    mock_service.save = AsyncMock(return_value=mock_account)
    use_case = CreateAccountUseCase(mock_service)

    # Act
    await use_case.execute(create_account_data)

    # Assert
    mock_service.save.assert_called_once()
    saved_account = mock_service.save.call_args[0][0]
    assert saved_account.balance == create_account_data.balance
    assert saved_account.type == create_account_data.type
