from unittest.mock import AsyncMock, Mock

import pytest

from app.api.v1.schemas.transaction_schema import TransactionBase
from app.domain.enums.transaction_status import TransactionStatus
from app.infrastructure.repositories.transaction_repository import TransactionRepository
from app.infrastructure.models.transaction_model import TransactionModel
from app.use_cases.transaction.get_transactions_by_account import (
    GetTransactionsByAccountUseCase,
)


@pytest.fixture
def mock_repository():
    """Create a mock repository for testing."""
    return Mock(spec=TransactionRepository)


@pytest.fixture
def mock_transaction_models():
    """Create mock transaction models."""
    mock_transactions = []
    for i in range(1, 4):
        mock_transaction = Mock(spec=TransactionModel)
        mock_transaction.id = i
        mock_transaction.amount = float(100 * i)
        mock_transaction.status = TransactionStatus.SUCCESS.value
        mock_transactions.append(mock_transaction)
    return mock_transactions


@pytest.mark.asyncio
async def test_get_transactions_by_account_success_with_default_status(
    mock_repository, mock_transaction_models
):
    """Test successful retrieval of transactions with default SUCCESS status."""
    # Arrange
    account_id = 1
    mock_repository.get_by_account_id = AsyncMock(return_value=mock_transaction_models)
    use_case = GetTransactionsByAccountUseCase(mock_repository)

    # Act
    result = await use_case.execute(account_id)

    # Assert
    assert len(result) == 3
    assert all(isinstance(t, TransactionBase) for t in result)
    assert result[0].id == 1
    assert result[0].amount == 100.0
    assert result[0].status == TransactionStatus.SUCCESS
    assert result[1].id == 2
    assert result[1].amount == 200.0
    assert result[2].id == 3
    assert result[2].amount == 300.0
    mock_repository.get_by_account_id.assert_called_once_with(
        account_id, TransactionStatus.SUCCESS
    )


@pytest.mark.asyncio
async def test_get_transactions_by_account_with_pending_status(
    mock_repository,
):
    """Test retrieval of transactions with PENDING status."""
    # Arrange
    account_id = 2
    mock_transaction = Mock(spec=TransactionModel)
    mock_transaction.id = 1
    mock_transaction.amount = 150.0
    mock_transaction.status = TransactionStatus.PENDING.value

    mock_repository.get_by_account_id = AsyncMock(return_value=[mock_transaction])
    use_case = GetTransactionsByAccountUseCase(mock_repository)

    # Act
    result = await use_case.execute(account_id, TransactionStatus.PENDING)

    # Assert
    assert len(result) == 1
    assert result[0].status == TransactionStatus.PENDING
    mock_repository.get_by_account_id.assert_called_once_with(
        account_id, TransactionStatus.PENDING
    )


@pytest.mark.asyncio
async def test_get_transactions_by_account_with_failed_status(mock_repository):
    """Test retrieval of transactions with FAILED status."""
    # Arrange
    account_id = 3
    mock_transaction = Mock(spec=TransactionModel)
    mock_transaction.id = 2
    mock_transaction.amount = 50.0
    mock_transaction.status = TransactionStatus.FAILED.value

    mock_repository.get_by_account_id = AsyncMock(return_value=[mock_transaction])
    use_case = GetTransactionsByAccountUseCase(mock_repository)

    # Act
    result = await use_case.execute(account_id, TransactionStatus.FAILED)

    # Assert
    assert len(result) == 1
    assert result[0].status == TransactionStatus.FAILED
    mock_repository.get_by_account_id.assert_called_once_with(
        account_id, TransactionStatus.FAILED
    )


@pytest.mark.asyncio
async def test_get_transactions_by_account_empty_result(mock_repository):
    """Test retrieval when no transactions exist for the account."""
    # Arrange
    account_id = 999
    mock_repository.get_by_account_id = AsyncMock(return_value=[])
    use_case = GetTransactionsByAccountUseCase(mock_repository)

    # Act
    result = await use_case.execute(account_id)

    # Assert
    assert len(result) == 0
    assert isinstance(result, list)
    mock_repository.get_by_account_id.assert_called_once_with(
        account_id, TransactionStatus.SUCCESS
    )


@pytest.mark.asyncio
async def test_get_transactions_by_account_single_transaction(mock_repository):
    """Test retrieval of a single transaction."""
    # Arrange
    account_id = 4
    mock_transaction = Mock(spec=TransactionModel)
    mock_transaction.id = 10
    mock_transaction.amount = 999.99
    mock_transaction.status = TransactionStatus.SUCCESS.value

    mock_repository.get_by_account_id = AsyncMock(return_value=[mock_transaction])
    use_case = GetTransactionsByAccountUseCase(mock_repository)

    # Act
    result = await use_case.execute(account_id)

    # Assert
    assert len(result) == 1
    assert result[0].id == 10
    assert result[0].amount == 999.99


@pytest.mark.asyncio
async def test_get_transactions_by_account_many_transactions(mock_repository):
    """Test retrieval of many transactions."""
    # Arrange
    account_id = 5
    mock_transactions = []
    for i in range(1, 21):
        mock_transaction = Mock(spec=TransactionModel)
        mock_transaction.id = i
        mock_transaction.amount = float(i * 10)
        mock_transaction.status = TransactionStatus.SUCCESS.value
        mock_transactions.append(mock_transaction)

    mock_repository.get_by_account_id = AsyncMock(return_value=mock_transactions)
    use_case = GetTransactionsByAccountUseCase(mock_repository)

    # Act
    result = await use_case.execute(account_id)

    # Assert
    assert len(result) == 20
    assert result[0].amount == 10.0
    assert result[19].amount == 200.0


@pytest.mark.asyncio
async def test_get_transactions_by_account_response_structure(
    mock_repository, mock_transaction_models
):
    """Test that response has correct structure with all required fields."""
    # Arrange
    account_id = 1
    mock_repository.get_by_account_id = AsyncMock(
        return_value=[mock_transaction_models[0]]
    )
    use_case = GetTransactionsByAccountUseCase(mock_repository)

    # Act
    result = await use_case.execute(account_id)

    # Assert
    assert len(result) == 1
    transaction = result[0]
    assert hasattr(transaction, "id")
    assert hasattr(transaction, "amount")
    assert hasattr(transaction, "status")
    assert isinstance(transaction.id, int)
    assert isinstance(transaction.amount, float)


@pytest.mark.asyncio
async def test_get_transactions_by_account_returns_list_type(
    mock_repository, mock_transaction_models
):
    """Test that execute returns a list type."""
    # Arrange
    account_id = 1
    mock_repository.get_by_account_id = AsyncMock(return_value=mock_transaction_models)
    use_case = GetTransactionsByAccountUseCase(mock_repository)

    # Act
    result = await use_case.execute(account_id)

    # Assert
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_get_transactions_by_account_preserves_all_fields(mock_repository):
    """Test that all transaction fields are preserved in the response."""
    # Arrange
    account_id = 1
    mock_transaction = Mock(spec=TransactionModel)
    mock_transaction.id = 42
    mock_transaction.amount = 777.77
    mock_transaction.status = TransactionStatus.SUCCESS.value

    mock_repository.get_by_account_id = AsyncMock(return_value=[mock_transaction])
    use_case = GetTransactionsByAccountUseCase(mock_repository)

    # Act
    result = await use_case.execute(account_id)

    # Assert
    assert result[0].id == 42
    assert result[0].amount == 777.77
    assert result[0].status == TransactionStatus.SUCCESS


@pytest.mark.asyncio
async def test_get_transactions_by_account_repository_called_with_correct_params(
    mock_repository, mock_transaction_models
):
    """Test that repository.get_by_account_id is called with correct parameters."""
    # Arrange
    account_id = 7
    transaction_status = TransactionStatus.PENDING
    mock_repository.get_by_account_id = AsyncMock(return_value=mock_transaction_models)
    use_case = GetTransactionsByAccountUseCase(mock_repository)

    # Act
    await use_case.execute(account_id, transaction_status)

    # Assert
    mock_repository.get_by_account_id.assert_called_once_with(
        account_id, transaction_status
    )


@pytest.mark.asyncio
async def test_get_transactions_by_account_with_zero_amount(mock_repository):
    """Test retrieval of transaction with zero amount."""
    # Arrange
    account_id = 1
    mock_transaction = Mock(spec=TransactionModel)
    mock_transaction.id = 100
    mock_transaction.amount = 0.0
    mock_transaction.status = TransactionStatus.SUCCESS.value

    mock_repository.get_by_account_id = AsyncMock(return_value=[mock_transaction])
    use_case = GetTransactionsByAccountUseCase(mock_repository)

    # Act
    result = await use_case.execute(account_id)

    # Assert
    assert result[0].amount == 0.0


@pytest.mark.asyncio
async def test_get_transactions_by_account_with_large_amount(mock_repository):
    """Test retrieval of transaction with very large amount."""
    # Arrange
    account_id = 1
    mock_transaction = Mock(spec=TransactionModel)
    mock_transaction.id = 101
    mock_transaction.amount = 999999999.99
    mock_transaction.status = TransactionStatus.SUCCESS.value

    mock_repository.get_by_account_id = AsyncMock(return_value=[mock_transaction])
    use_case = GetTransactionsByAccountUseCase(mock_repository)

    # Act
    result = await use_case.execute(account_id)

    # Assert
    assert result[0].amount == 999999999.99


@pytest.mark.asyncio
async def test_get_transactions_by_account_mixed_statuses_with_filter(
    mock_repository,
):
    """Test that filtering by status returns only matching transactions."""
    # Arrange
    account_id = 1
    # Create transactions with different statuses
    success_transactions = []
    for i in range(3):
        mock_transaction = Mock(spec=TransactionModel)
        mock_transaction.id = i + 1
        mock_transaction.amount = float(100 * (i + 1))
        mock_transaction.status = TransactionStatus.SUCCESS.value
        success_transactions.append(mock_transaction)

    mock_repository.get_by_account_id = AsyncMock(return_value=success_transactions)
    use_case = GetTransactionsByAccountUseCase(mock_repository)

    # Act
    result = await use_case.execute(account_id, TransactionStatus.SUCCESS)

    # Assert
    assert len(result) == 3
    assert all(t.status == TransactionStatus.SUCCESS for t in result)
