"""Unit tests for Account entity."""

from datetime import datetime, timezone

import pytest

from app.domain.entities.account import Account
from app.domain.entities.transaction import Transaction
from app.domain.enums.transaction_status import TransactionStatus


@pytest.mark.asyncio
async def test_account_creation_with_defaults():
    """Test that Account can be created with default values."""
    account = Account(id=1, balance=500.0)

    assert account.id == 1
    assert account.balance == 500.0
    assert account.type == "checking"
    assert account.created_at is not None
    assert account.updated_at is not None


@pytest.mark.asyncio
async def test_account_type_defaults_to_checking():
    """Test that account type defaults to 'checking'."""
    account = Account(id=1, balance=100.0)

    assert account.type == "checking"


@pytest.mark.asyncio
async def test_account_with_savings_type():
    """Test that account can be created with 'savings' type."""
    account = Account(id=2, balance=1000.0, type="savings")

    assert account.type == "savings"


@pytest.mark.asyncio
async def test_account_rejects_invalid_type():
    """Test that account rejects invalid account types."""
    with pytest.raises(ValueError):
        Account(id=1, balance=100.0, type="invalid_type")


@pytest.mark.asyncio
async def test_account_balance_can_be_zero():
    """Test that account balance can be zero."""
    account = Account(id=1, balance=0.0)

    assert account.balance == 0.0


@pytest.mark.asyncio
async def test_account_balance_can_be_negative():
    """Test that account balance can be negative (overdraft)."""
    account = Account(id=1, balance=-100.50)

    assert account.balance == -100.50


@pytest.mark.asyncio
async def test_account_with_float_balance():
    """Test account with fractional balance."""
    account = Account(id=1, balance=1234.56)

    assert account.balance == 1234.56


@pytest.mark.asyncio
async def test_account_created_at_auto_generated():
    """Test that created_at is auto-generated."""
    before = datetime.now(timezone.utc)
    account = Account(id=1, balance=100.0)
    after = datetime.now(timezone.utc)

    assert before <= account.created_at <= after


@pytest.mark.asyncio
async def test_account_updated_at_auto_generated():
    """Test that updated_at is auto-generated."""
    before = datetime.now(timezone.utc)
    account = Account(id=1, balance=100.0)
    after = datetime.now(timezone.utc)

    assert before <= account.updated_at <= after


@pytest.mark.asyncio
async def test_account_with_custom_created_at():
    """Test that account can be created with custom created_at."""
    custom_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    account = Account(id=1, balance=100.0, created_at=custom_time)

    assert account.created_at == custom_time


@pytest.mark.asyncio
async def test_account_with_transactions_list():
    """Test that account can hold a list of transactions."""
    transactions = [
        Transaction(id=1, amount=100.0, status=TransactionStatus.SUCCESS, account_id=1),
        Transaction(id=2, amount=50.0, status=TransactionStatus.PENDING, account_id=1),
    ]
    account = Account(id=1, balance=500.0, transactions=transactions)

    assert len(account.transactions) == 2
    assert account.transactions[0].amount == 100.0
    assert account.transactions[1].amount == 50.0


@pytest.mark.asyncio
async def test_account_with_none_transactions():
    """Test that account transactions can be None."""
    account = Account(id=1, balance=100.0, transactions=None)

    assert account.transactions is None


@pytest.mark.asyncio
async def test_account_with_empty_transactions_list():
    """Test that account can have empty transactions list."""
    account = Account(id=1, balance=100.0, transactions=[])

    assert account.transactions == []
    assert len(account.transactions) == 0


@pytest.mark.asyncio
async def test_account_without_id():
    """Test that account can be created without ID (before persistence)."""
    account = Account(balance=100.0)

    assert account.id is None
    assert account.balance == 100.0


@pytest.mark.asyncio
async def test_account_model_validation_fails_with_invalid_balance():
    """Test that account validates balance type."""
    with pytest.raises(ValueError):
        Account(id=1, balance="not-a-number")


@pytest.mark.asyncio
async def test_account_equality():
    """Test account equality based on all fields."""
    account1 = Account(id=1, balance=500.0, type="checking")
    account2 = Account(id=1, balance=500.0, type="checking")

    # Pydantic models should have the same field values but different instances
    assert account1.id == account2.id
    assert account1.balance == account2.balance
    assert account1.type == account2.type


@pytest.mark.asyncio
async def test_account_large_balance():
    """Test account with large balance values."""
    large_balance = 999999999.99
    account = Account(id=1, balance=large_balance)

    assert account.balance == large_balance


@pytest.mark.asyncio
async def test_account_very_small_balance():
    """Test account with very small balance values."""
    small_balance = 0.01
    account = Account(id=1, balance=small_balance)

    assert account.balance == small_balance


@pytest.mark.asyncio
async def test_account_both_account_types():
    """Test both valid account types."""
    checking = Account(id=1, balance=100.0, type="checking")
    savings = Account(id=2, balance=200.0, type="savings")

    assert checking.type == "checking"
    assert savings.type == "savings"
    assert checking.type != savings.type
