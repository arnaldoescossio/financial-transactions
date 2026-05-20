"""Unit tests for AccountService."""

from unittest.mock import AsyncMock, Mock

import pytest

from app.domain.entities.account import Account
from app.domain.service.account_service import AccountService


@pytest.fixture
def mock_account_repo():
    """Create a mock account repository for testing."""
    return Mock()


@pytest.fixture
def account_service(mock_account_repo):
    """Create an AccountService with mocked repository."""
    return AccountService(mock_account_repo)


@pytest.fixture
def sample_account():
    """Create a sample account entity for testing."""
    return Account(
        id=1,
        balance=500.0,
        type="checking",
    )


@pytest.fixture
def sample_unsaved_account():
    """Create a sample account without ID (before persistence)."""
    return Account(
        balance=750.0,
        type="savings",
    )


@pytest.mark.asyncio
async def test_save_account_returns_created_account(
    account_service, mock_account_repo, sample_unsaved_account
):
    """Test that save returns the created account with ID."""
    expected = Account(
        id=1,
        balance=sample_unsaved_account.balance,
        type=sample_unsaved_account.type,
    )

    mock_account_repo.save = AsyncMock(return_value=expected)
    account_service._accounts = mock_account_repo

    result = await account_service.save(sample_unsaved_account)

    assert isinstance(result, Account)
    assert result.id == 1
    assert result.balance == sample_unsaved_account.balance
    assert result.type == sample_unsaved_account.type

    mock_account_repo.save.assert_awaited_once_with(sample_unsaved_account)


@pytest.mark.asyncio
async def test_save_account_delegates_to_repository(
    account_service, mock_account_repo, sample_unsaved_account
):
    """Test that save delegates to the repository."""
    expected = Account(id=5, balance=100.0, type="checking")
    mock_account_repo.save = AsyncMock(return_value=expected)
    account_service._accounts = mock_account_repo

    await account_service.save(sample_unsaved_account)

    mock_account_repo.save.assert_awaited_once()
    called_account = mock_account_repo.save.call_args[0][0]
    assert called_account.balance == sample_unsaved_account.balance


@pytest.mark.asyncio
async def test_save_account_with_checking_type(account_service, mock_account_repo):
    """Test saving an account with checking type."""
    account = Account(balance=1000.0, type="checking")
    expected = Account(id=10, balance=1000.0, type="checking")

    mock_account_repo.save = AsyncMock(return_value=expected)
    account_service._accounts = mock_account_repo

    result = await account_service.save(account)

    assert result.type == "checking"
    mock_account_repo.save.assert_awaited_once()


@pytest.mark.asyncio
async def test_save_account_with_savings_type(account_service, mock_account_repo):
    """Test saving an account with savings type."""
    account = Account(balance=2000.0, type="savings")
    expected = Account(id=11, balance=2000.0, type="savings")

    mock_account_repo.save = AsyncMock(return_value=expected)
    account_service._accounts = mock_account_repo

    result = await account_service.save(account)

    assert result.type == "savings"
    mock_account_repo.save.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_by_id_returns_account(
    account_service, mock_account_repo, sample_account
):
    """Test that get_by_id returns the account."""
    mock_account_repo.get_by_id = AsyncMock(return_value=sample_account)
    account_service._accounts = mock_account_repo

    result = await account_service.get_by_id(1)

    assert isinstance(result, Account)
    assert result.id == sample_account.id
    assert result.balance == sample_account.balance

    mock_account_repo.get_by_id.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_get_by_id_delegates_to_repository(account_service, mock_account_repo):
    """Test that get_by_id delegates to the repository."""
    expected = Account(id=42, balance=555.55, type="savings")
    mock_account_repo.get_by_id = AsyncMock(return_value=expected)
    account_service._accounts = mock_account_repo

    result = await account_service.get_by_id(42)

    assert result.id == 42
    mock_account_repo.get_by_id.assert_awaited_once_with(42)


@pytest.mark.asyncio
async def test_get_by_id_with_different_ids(account_service, mock_account_repo):
    """Test get_by_id with multiple different account IDs."""
    test_ids = [1, 5, 10, 100, 999]

    for account_id in test_ids:
        expected = Account(id=account_id, balance=100.0 * account_id)
        mock_account_repo.get_by_id = AsyncMock(return_value=expected)
        account_service._accounts = mock_account_repo

        result = await account_service.get_by_id(account_id)

        assert result.id == account_id
        mock_account_repo.get_by_id.assert_awaited_with(account_id)


@pytest.mark.asyncio
async def test_save_multiple_accounts_in_sequence(account_service, mock_account_repo):
    """Test saving multiple accounts in sequence."""
    accounts = [
        Account(balance=100.0, type="checking"),
        Account(balance=200.0, type="savings"),
        Account(balance=300.0, type="checking"),
    ]

    created = [
        Account(id=1, balance=100.0, type="checking"),
        Account(id=2, balance=200.0, type="savings"),
        Account(id=3, balance=300.0, type="checking"),
    ]

    mock_account_repo.save = AsyncMock(side_effect=created)
    account_service._accounts = mock_account_repo

    results = []
    for account in accounts:
        result = await account_service.save(account)
        results.append(result)

    assert len(results) == 3
    assert all(isinstance(r, Account) for r in results)
    assert mock_account_repo.save.await_count == 3


@pytest.mark.asyncio
async def test_save_preserves_account_balance(account_service, mock_account_repo):
    """Test that save preserves the account balance."""
    balance = 12345.67
    account = Account(balance=balance, type="checking")
    expected = Account(id=1, balance=balance, type="checking")

    mock_account_repo.save = AsyncMock(return_value=expected)
    account_service._accounts = mock_account_repo

    result = await account_service.save(account)

    assert result.balance == balance


@pytest.mark.asyncio
async def test_get_by_id_with_zero_balance(account_service, mock_account_repo):
    """Test get_by_id with zero balance account."""
    account = Account(id=1, balance=0.0, type="checking")
    mock_account_repo.get_by_id = AsyncMock(return_value=account)
    account_service._accounts = mock_account_repo

    result = await account_service.get_by_id(1)

    assert result.balance == 0.0


@pytest.mark.asyncio
async def test_get_by_id_with_negative_balance(account_service, mock_account_repo):
    """Test get_by_id with negative balance account (overdraft)."""
    account = Account(id=1, balance=-500.0, type="checking")
    mock_account_repo.get_by_id = AsyncMock(return_value=account)
    account_service._accounts = mock_account_repo

    result = await account_service.get_by_id(1)

    assert result.balance == -500.0
