"""Unit tests for TransactionService."""

from unittest.mock import AsyncMock, Mock

import pytest

from app.domain.entities.transaction import Transaction
from app.domain.enums.transaction_status import TransactionStatus
from app.domain.service.transaction_service import TransactionService


@pytest.fixture
def mock_transaction_repo():
    """Create a mock transaction repository for testing."""
    return Mock()


@pytest.fixture
def transaction_service(mock_transaction_repo):
    """Create a TransactionService with mocked repository."""
    return TransactionService(mock_transaction_repo)


@pytest.fixture
def sample_transaction():
    """Create a sample transaction entity for testing."""
    return Transaction(
        id=1,
        amount=100.0,
        status=TransactionStatus.SUCCESS,
        account_id=1,
    )


@pytest.fixture
def sample_unsaved_transaction():
    """Create a sample transaction without ID (before persistence)."""
    return Transaction(
        amount=250.0,
        status=TransactionStatus.PENDING,
        account_id=2,
    )


@pytest.mark.asyncio
async def test_save_transaction_returns_created_transaction(
    transaction_service, mock_transaction_repo, sample_unsaved_transaction
):
    """Test that save returns the created transaction with ID."""
    expected = Transaction(
        id=1,
        amount=sample_unsaved_transaction.amount,
        status=sample_unsaved_transaction.status,
        account_id=sample_unsaved_transaction.account_id,
    )

    mock_transaction_repo.save = AsyncMock(return_value=expected)
    transaction_service._transactions = mock_transaction_repo

    result = await transaction_service.save(sample_unsaved_transaction)

    assert isinstance(result, Transaction)
    assert result.id == 1
    assert result.amount == sample_unsaved_transaction.amount
    assert result.status == sample_unsaved_transaction.status

    mock_transaction_repo.save.assert_awaited_once_with(sample_unsaved_transaction)


@pytest.mark.asyncio
async def test_save_transaction_delegates_to_repository(
    transaction_service, mock_transaction_repo, sample_unsaved_transaction
):
    """Test that save delegates to the repository."""
    expected = Transaction(
        id=5,
        amount=150.0,
        status=TransactionStatus.SUCCESS,
        account_id=1,
    )
    mock_transaction_repo.save = AsyncMock(return_value=expected)
    transaction_service._transactions = mock_transaction_repo

    await transaction_service.save(sample_unsaved_transaction)

    mock_transaction_repo.save.assert_awaited_once()
    called_transaction = mock_transaction_repo.save.call_args[0][0]
    assert called_transaction.amount == sample_unsaved_transaction.amount


@pytest.mark.asyncio
async def test_save_transaction_with_success_status(
    transaction_service, mock_transaction_repo
):
    """Test saving a transaction with SUCCESS status."""
    transaction = Transaction(
        amount=100.0,
        status=TransactionStatus.SUCCESS,
        account_id=1,
    )
    expected = Transaction(
        id=10,
        amount=100.0,
        status=TransactionStatus.SUCCESS,
        account_id=1,
    )

    mock_transaction_repo.save = AsyncMock(return_value=expected)
    transaction_service._transactions = mock_transaction_repo

    result = await transaction_service.save(transaction)

    assert result.status == TransactionStatus.SUCCESS
    mock_transaction_repo.save.assert_awaited_once()


@pytest.mark.asyncio
async def test_save_transaction_with_pending_status(
    transaction_service, mock_transaction_repo
):
    """Test saving a transaction with PENDING status."""
    transaction = Transaction(
        amount=200.0,
        status=TransactionStatus.PENDING,
        account_id=2,
    )
    expected = Transaction(
        id=11,
        amount=200.0,
        status=TransactionStatus.PENDING,
        account_id=2,
    )

    mock_transaction_repo.save = AsyncMock(return_value=expected)
    transaction_service._transactions = mock_transaction_repo

    result = await transaction_service.save(transaction)

    assert result.status == TransactionStatus.PENDING
    mock_transaction_repo.save.assert_awaited_once()


@pytest.mark.asyncio
async def test_save_transaction_with_failed_status(
    transaction_service, mock_transaction_repo
):
    """Test saving a transaction with FAILED status."""
    transaction = Transaction(
        amount=50.0,
        status=TransactionStatus.FAILED,
        account_id=3,
    )
    expected = Transaction(
        id=12,
        amount=50.0,
        status=TransactionStatus.FAILED,
        account_id=3,
    )

    mock_transaction_repo.save = AsyncMock(return_value=expected)
    transaction_service._transactions = mock_transaction_repo

    result = await transaction_service.save(transaction)

    assert result.status == TransactionStatus.FAILED
    mock_transaction_repo.save.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_transactions_by_account_id_success(
    transaction_service, mock_transaction_repo
):
    """Test getting transactions by account ID with SUCCESS status (default)."""
    transactions = [
        Transaction(
            id=1,
            amount=100.0,
            status=TransactionStatus.SUCCESS,
            account_id=1,
        ),
        Transaction(
            id=2,
            amount=200.0,
            status=TransactionStatus.SUCCESS,
            account_id=1,
        ),
    ]

    mock_transaction_repo.get_by_account_id = AsyncMock(return_value=transactions)
    transaction_service._transactions = mock_transaction_repo

    result = await transaction_service.get_transactions_by_account_id(account_id=1)

    assert len(result) == 2
    assert all(t.status == TransactionStatus.SUCCESS for t in result)
    mock_transaction_repo.get_by_account_id.assert_awaited_once_with(
        1, TransactionStatus.SUCCESS
    )


@pytest.mark.asyncio
async def test_get_transactions_by_account_id_with_specific_status(
    transaction_service, mock_transaction_repo
):
    """Test getting transactions by account ID with specific status."""
    transactions = [
        Transaction(
            id=1,
            amount=100.0,
            status=TransactionStatus.PENDING,
            account_id=1,
        ),
    ]

    mock_transaction_repo.get_by_account_id = AsyncMock(return_value=transactions)
    transaction_service._transactions = mock_transaction_repo

    result = await transaction_service.get_transactions_by_account_id(
        account_id=1,
        transaction_status=TransactionStatus.PENDING,
    )

    assert len(result) == 1
    assert result[0].status == TransactionStatus.PENDING
    mock_transaction_repo.get_by_account_id.assert_awaited_once_with(
        1, TransactionStatus.PENDING
    )


@pytest.mark.asyncio
async def test_get_transactions_by_account_id_empty_result(
    transaction_service, mock_transaction_repo
):
    """Test getting transactions by account ID returns empty list."""
    mock_transaction_repo.get_by_account_id = AsyncMock(return_value=[])
    transaction_service._transactions = mock_transaction_repo

    result = await transaction_service.get_transactions_by_account_id(account_id=999)

    assert len(result) == 0
    assert result == []
    mock_transaction_repo.get_by_account_id.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_transactions_by_account_id_delegates_to_repository(
    transaction_service, mock_transaction_repo
):
    """Test that get_transactions_by_account_id delegates to repository."""
    expected = [
        Transaction(
            id=1,
            amount=50.0,
            status=TransactionStatus.SUCCESS,
            account_id=5,
        )
    ]
    mock_transaction_repo.get_by_account_id = AsyncMock(return_value=expected)
    transaction_service._transactions = mock_transaction_repo

    await transaction_service.get_transactions_by_account_id(account_id=5)

    mock_transaction_repo.get_by_account_id.assert_awaited_once()
    call_args = mock_transaction_repo.get_by_account_id.call_args[0]
    assert call_args[0] == 5
    assert call_args[1] == TransactionStatus.SUCCESS


@pytest.mark.asyncio
async def test_get_transactions_with_failed_status(
    transaction_service, mock_transaction_repo
):
    """Test getting transactions with FAILED status."""
    transactions = [
        Transaction(
            id=1,
            amount=100.0,
            status=TransactionStatus.FAILED,
            account_id=1,
        ),
    ]

    mock_transaction_repo.get_by_account_id = AsyncMock(return_value=transactions)
    transaction_service._transactions = mock_transaction_repo

    result = await transaction_service.get_transactions_by_account_id(
        account_id=1,
        transaction_status=TransactionStatus.FAILED,
    )

    assert len(result) == 1
    assert result[0].status == TransactionStatus.FAILED


@pytest.mark.asyncio
async def test_save_multiple_transactions_in_sequence(
    transaction_service, mock_transaction_repo
):
    """Test saving multiple transactions in sequence."""
    transactions = [
        Transaction(amount=100.0, status=TransactionStatus.SUCCESS, account_id=1),
        Transaction(amount=200.0, status=TransactionStatus.PENDING, account_id=2),
        Transaction(amount=50.0, status=TransactionStatus.FAILED, account_id=3),
    ]

    created = [
        Transaction(id=1, amount=100.0, status=TransactionStatus.SUCCESS, account_id=1),
        Transaction(id=2, amount=200.0, status=TransactionStatus.PENDING, account_id=2),
        Transaction(id=3, amount=50.0, status=TransactionStatus.FAILED, account_id=3),
    ]

    mock_transaction_repo.save = AsyncMock(side_effect=created)
    transaction_service._transactions = mock_transaction_repo

    results = []
    for tx in transactions:
        result = await transaction_service.save(tx)
        results.append(result)

    assert len(results) == 3
    assert all(isinstance(r, Transaction) for r in results)
    assert mock_transaction_repo.save.await_count == 3


@pytest.mark.asyncio
async def test_save_transaction_preserves_amount(
    transaction_service, mock_transaction_repo
):
    """Test that save preserves the transaction amount."""
    amount = 1234.56
    transaction = Transaction(
        amount=amount,
        status=TransactionStatus.SUCCESS,
        account_id=1,
    )
    expected = Transaction(
        id=1,
        amount=amount,
        status=TransactionStatus.SUCCESS,
        account_id=1,
    )

    mock_transaction_repo.save = AsyncMock(return_value=expected)
    transaction_service._transactions = mock_transaction_repo

    result = await transaction_service.save(transaction)

    assert result.amount == amount


@pytest.mark.asyncio
async def test_get_transactions_multiple_transactions_same_account(
    transaction_service, mock_transaction_repo
):
    """Test getting multiple transactions for the same account."""
    transactions = [
        Transaction(
            id=1,
            amount=100.0,
            status=TransactionStatus.SUCCESS,
            account_id=1,
        ),
        Transaction(
            id=2,
            amount=50.0,
            status=TransactionStatus.SUCCESS,
            account_id=1,
        ),
        Transaction(
            id=3,
            amount=75.0,
            status=TransactionStatus.SUCCESS,
            account_id=1,
        ),
    ]

    mock_transaction_repo.get_by_account_id = AsyncMock(return_value=transactions)
    transaction_service._transactions = mock_transaction_repo

    result = await transaction_service.get_transactions_by_account_id(account_id=1)

    assert len(result) == 3
    assert all(t.account_id == 1 for t in result)
