from unittest.mock import AsyncMock, Mock

import pytest

from app.domain.entities.account import AccountResponse
from app.domain.exceptions.account_not_found import AccountNotFoundException
from app.domain.repositories.account_repository import AccountRepository
from app.infrastructure.models.account_model import AccountModel
from app.infrastructure.models.transaction_model import TransactionModel
from app.use_cases.account.get_account import GetAccountUseCase


@pytest.fixture
def mock_repository():
    """Create a mock account repository for testing."""
    return Mock(spec=AccountRepository)


@pytest.fixture
def mock_account_with_transactions():
    """Create a mock account model with related transactions."""
    tx1 = Mock(spec=TransactionModel)
    tx1.id = 1
    tx1.amount = 100.0
    tx1.status = "SUCCESS"

    tx2 = Mock(spec=TransactionModel)
    tx2.id = 2
    tx2.amount = 50.0
    tx2.status = "PENDING"

    account = Mock(spec=AccountModel)
    account.id = 10
    account.balance = 1500.0
    account.type = "checking"
    account.transactions = [tx1, tx2]

    return account


@pytest.mark.asyncio
async def test_get_account_success(mock_repository, mock_account_with_transactions):
    """Test successful account retrieval with mapped transactions."""
    # Arrange
    account_id = 10
    mock_repository.get_by_id = AsyncMock(return_value=mock_account_with_transactions)
    use_case = GetAccountUseCase(mock_repository)

    # Act
    result = await use_case.execute(account_id)

    # Assert
    assert isinstance(result, AccountResponse)
    assert result.id == 10
    assert result.balance == 1500.0
    assert result.type == "checking"
    assert isinstance(result.transactions, list)
    assert len(result.transactions) == 2
    assert result.transactions[0]["id"] == 1
    assert result.transactions[0]["amount"] == 100.0
    assert result.transactions[0]["status"] == "SUCCESS"
    assert result.transactions[1]["id"] == 2
    assert result.transactions[1]["amount"] == 50.0
    assert result.transactions[1]["status"] == "PENDING"
    mock_repository.get_by_id.assert_called_once_with(account_id)


@pytest.mark.asyncio
async def test_get_account_not_found_raises_exception(mock_repository):
    """Test that missing account raises AccountNotFoundException."""
    # Arrange
    account_id = 999
    mock_repository.get_by_id = AsyncMock(return_value=None)
    use_case = GetAccountUseCase(mock_repository)

    # Act / Assert
    with pytest.raises(AccountNotFoundException) as exc_info:
        await use_case.execute(account_id)

    assert "Account not found" in str(exc_info.value)
    mock_repository.get_by_id.assert_called_once_with(account_id)


@pytest.mark.asyncio
async def test_get_account_repository_called_with_correct_id(
    mock_repository, mock_account_with_transactions
):
    """Test that repository.get_by_id receives the provided account id."""
    # Arrange
    account_id = 42
    mock_repository.get_by_id = AsyncMock(return_value=mock_account_with_transactions)
    use_case = GetAccountUseCase(mock_repository)

    # Act
    await use_case.execute(account_id)

    # Assert
    mock_repository.get_by_id.assert_called_once()
    assert mock_repository.get_by_id.call_args[0][0] == account_id
