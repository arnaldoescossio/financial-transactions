"""Unit tests for Transaction entity."""

from datetime import datetime, timezone

import pytest

from app.domain.entities.transaction import Transaction
from app.domain.enums.transaction_status import TransactionStatus


@pytest.mark.asyncio
async def test_transaction_creation_with_defaults():
    """Test that Transaction can be created with default values."""
    transaction = Transaction(
        id=1,
        amount=100.0,
        status=TransactionStatus.SUCCESS,
        account_id=1,
    )

    assert transaction.id == 1
    assert transaction.amount == 100.0
    assert transaction.status == TransactionStatus.SUCCESS
    assert transaction.account_id == 1


@pytest.mark.asyncio
async def test_transaction_created_at_auto_generated():
    """Test that created_at is auto-generated."""
    before = datetime.now(timezone.utc)
    transaction = Transaction(
        id=1,
        amount=50.0,
        status=TransactionStatus.PENDING,
    )
    after = datetime.now(timezone.utc)

    assert before <= transaction.created_at <= after


@pytest.mark.asyncio
async def test_transaction_updated_at_auto_generated():
    """Test that updated_at is auto-generated."""
    before = datetime.now(timezone.utc)
    transaction = Transaction(
        id=1,
        amount=50.0,
        status=TransactionStatus.PENDING,
    )
    after = datetime.now(timezone.utc)

    assert before <= transaction.updated_at <= after


@pytest.mark.asyncio
async def test_transaction_without_id():
    """Test that Transaction can be created without ID (before persistence)."""
    transaction = Transaction(
        amount=100.0,
        status=TransactionStatus.SUCCESS,
        account_id=1,
    )

    assert transaction.id is None
    assert transaction.amount == 100.0


@pytest.mark.asyncio
async def test_transaction_with_all_statuses():
    """Test Transaction with all valid statuses."""
    for status in TransactionStatus:
        transaction = Transaction(
            id=1,
            amount=100.0,
            status=status,
            account_id=1,
        )

        assert transaction.status == status


@pytest.mark.asyncio
async def test_transaction_amount_validation_allows_zero():
    """Test that transaction amount can be zero."""
    transaction = Transaction(
        id=1,
        amount=0.0,
        status=TransactionStatus.SUCCESS,
        account_id=1,
    )

    assert transaction.amount == 0.0


@pytest.mark.asyncio
async def test_transaction_amount_validation_rejects_negative():
    """Test that transaction amount cannot be negative."""
    with pytest.raises(ValueError):
        Transaction(
            id=1,
            amount=-100.0,
            status=TransactionStatus.SUCCESS,
            account_id=1,
        )


@pytest.mark.asyncio
async def test_transaction_amount_with_fractional_values():
    """Test transaction with fractional amount values."""
    transaction = Transaction(
        id=1,
        amount=123.45,
        status=TransactionStatus.SUCCESS,
        account_id=1,
    )

    assert transaction.amount == 123.45


@pytest.mark.asyncio
async def test_transaction_is_valid_property_success():
    """Test is_valid property returns True for successful transaction with positive amount."""
    transaction = Transaction(
        id=1,
        amount=100.0,
        status=TransactionStatus.SUCCESS,
        account_id=1,
    )

    assert transaction.is_valid is True


@pytest.mark.asyncio
async def test_transaction_is_valid_property_zero_amount():
    """Test is_valid property returns False for zero amount."""
    transaction = Transaction(
        id=1,
        amount=0.0,
        status=TransactionStatus.SUCCESS,
        account_id=1,
    )

    assert transaction.is_valid is False


@pytest.mark.asyncio
async def test_transaction_is_valid_property_pending():
    """Test is_valid property returns False for pending status."""
    transaction = Transaction(
        id=1,
        amount=100.0,
        status=TransactionStatus.PENDING,
        account_id=1,
    )

    assert transaction.is_valid is False


@pytest.mark.asyncio
async def test_transaction_is_valid_property_failed():
    """Test is_valid property returns False for failed status."""
    transaction = Transaction(
        id=1,
        amount=100.0,
        status=TransactionStatus.FAILED,
        account_id=1,
    )

    assert transaction.is_valid is False


@pytest.mark.asyncio
async def test_transaction_is_failed_property_true():
    """Test is_failed property returns True for failed status."""
    transaction = Transaction(
        id=1,
        amount=100.0,
        status=TransactionStatus.FAILED,
        account_id=1,
    )

    assert transaction.is_failed is True


@pytest.mark.asyncio
async def test_transaction_is_failed_property_false():
    """Test is_failed property returns False for non-failed statuses."""
    for status in [TransactionStatus.SUCCESS, TransactionStatus.PENDING]:
        transaction = Transaction(
            id=1,
            amount=100.0,
            status=status,
            account_id=1,
        )

        assert transaction.is_failed is False


@pytest.mark.asyncio
async def test_transaction_with_account_reference():
    """Test Transaction with account relationship."""
    from app.domain.entities.account import Account

    account = Account(id=1, balance=500.0)
    transaction = Transaction(
        id=1,
        amount=100.0,
        status=TransactionStatus.SUCCESS,
        account=account,
        account_id=1,
    )

    assert transaction.account == account
    assert transaction.account_id == 1


@pytest.mark.asyncio
async def test_transaction_with_custom_created_at():
    """Test that transaction can be created with custom created_at."""
    custom_time = datetime(2024, 1, 15, 10, 30, 0, tzinfo=timezone.utc)
    transaction = Transaction(
        id=1,
        amount=100.0,
        status=TransactionStatus.SUCCESS,
        created_at=custom_time,
        account_id=1,
    )

    assert transaction.created_at == custom_time


@pytest.mark.asyncio
async def test_transaction_with_large_amount():
    """Test transaction with large amount values."""
    large_amount = 999999999.99
    transaction = Transaction(
        id=1,
        amount=large_amount,
        status=TransactionStatus.SUCCESS,
        account_id=1,
    )

    assert transaction.amount == large_amount


@pytest.mark.asyncio
async def test_transaction_with_very_small_amount():
    """Test transaction with very small amount values."""
    small_amount = 0.01
    transaction = Transaction(
        id=1,
        amount=small_amount,
        status=TransactionStatus.SUCCESS,
        account_id=1,
    )

    assert transaction.amount == small_amount


@pytest.mark.asyncio
async def test_transaction_account_id_none():
    """Test transaction without account_id."""
    transaction = Transaction(
        id=1,
        amount=100.0,
        status=TransactionStatus.SUCCESS,
        account_id=None,
    )

    assert transaction.account_id is None


@pytest.mark.asyncio
async def test_transaction_status_can_be_none():
    """Test transaction with None status (before validation)."""
    transaction = Transaction(
        id=1,
        amount=100.0,
        status=None,
        account_id=1,
    )

    assert transaction.status is None


@pytest.mark.asyncio
async def test_transaction_amount_can_be_none():
    """Test transaction with None amount (before validation)."""
    transaction = Transaction(
        id=1,
        amount=None,
        status=TransactionStatus.SUCCESS,
        account_id=1,
    )

    assert transaction.amount is None


@pytest.mark.asyncio
async def test_transaction_is_valid_with_none_values():
    """Test is_valid property when status or amount is None."""
    transaction = Transaction(
        id=1,
        amount=None,
        status=None,
        account_id=1,
    )

    assert transaction.is_valid is False


@pytest.mark.asyncio
async def test_transaction_serialization_to_dict():
    """Test that Transaction can be serialized to dictionary."""
    transaction = Transaction(
        id=1,
        amount=100.0,
        status=TransactionStatus.SUCCESS,
        account_id=1,
    )

    tx_dict = transaction.model_dump()

    assert tx_dict["id"] == 1
    assert tx_dict["amount"] == 100.0
    assert tx_dict["status"] == TransactionStatus.SUCCESS
    assert tx_dict["account_id"] == 1
