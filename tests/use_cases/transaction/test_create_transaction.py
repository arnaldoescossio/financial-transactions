from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, Mock

import pytest
from asyncpg import exceptions
from sqlalchemy.exc import IntegrityError

from app.domain.entities.transaction import TransactionCreate, TransactionResponse
from app.domain.enums.transaction_status import TransactionStatus
from app.domain.exceptions.account_not_found import AccountNotFoundException
from app.domain.repositories.transaction_repository import TransactionRepository
from app.infrastructure.models.account_model import AccountModel
from app.infrastructure.models.transaction_model import TransactionModel
from app.use_cases.transaction.create_transaction import CreateTransactionUseCase


@pytest.fixture
def mock_repository():
    """Create a mock repository for testing."""
    return Mock(spec=TransactionRepository)


@pytest.fixture
def create_transaction_data():
    """Create sample transaction data for testing."""
    return TransactionCreate(
        amount=100.0,
        status=TransactionStatus.SUCCESS,
        account_id=1,
    )


@pytest.fixture
def mock_transaction_model():
    """Create a mock transaction model with account relationship."""
    mock_account = Mock(spec=AccountModel)
    mock_account.id = 1
    mock_account.balance = 1000.0
    mock_account.type = "checking"

    mock_transaction = Mock(spec=TransactionModel)
    mock_transaction.id = 1
    mock_transaction.amount = 100.0
    mock_transaction.status = "SUCCESS"
    mock_transaction.account = mock_account
    mock_transaction.created_at = datetime.now()
    mock_transaction.updated_at = datetime.now()

    return mock_transaction


@pytest.mark.asyncio
async def test_create_transaction_success(
    mock_repository, create_transaction_data, mock_transaction_model
):
    """Test successful transaction creation."""
    # Arrange
    mock_repository.save = AsyncMock(return_value=mock_transaction_model)
    use_case = CreateTransactionUseCase(mock_repository)

    # Act
    result = await use_case.execute(create_transaction_data)

    # Assert
    assert isinstance(result, TransactionResponse)
    assert result.id == 1
    assert result.amount == 100.0
    assert result.status == TransactionStatus.SUCCESS
    assert result.account.id == 1
    assert result.account.balance == 1000.0
    assert result.account.type == "checking"
    mock_repository.save.assert_called_once_with(create_transaction_data)


@pytest.mark.asyncio
async def test_create_transaction_with_account_not_found(
    mock_repository, create_transaction_data
):
    """Test transaction creation fails when account is not found (foreign key violation)."""
    # Arrange
    foreign_key_error = exceptions.ForeignKeyViolationError("account_id")
    integrity_error = IntegrityError(
        statement="INSERT INTO transactions...",
        params={},
        orig=MagicMock(__cause__=foreign_key_error),
    )

    mock_repository.save = AsyncMock(side_effect=integrity_error)
    use_case = CreateTransactionUseCase(mock_repository)

    # Act & Assert
    with pytest.raises(AccountNotFoundException) as exc_info:
        await use_case.execute(create_transaction_data)

    assert "Failed to create transaction: Account not found" in str(exc_info.value)
    mock_repository.save.assert_called_once_with(create_transaction_data)


@pytest.mark.asyncio
async def test_create_transaction_with_generic_integrity_error(
    mock_repository, create_transaction_data
):
    """Test transaction creation with generic integrity error (not foreign key)."""
    # Arrange
    integrity_error = IntegrityError(
        statement="INSERT INTO transactions...",
        params={},
        orig=MagicMock(__cause__=Exception("Some other integrity error")),
    )

    mock_repository.save = AsyncMock(side_effect=integrity_error)
    use_case = CreateTransactionUseCase(mock_repository)

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        await use_case.execute(create_transaction_data)

    assert "Failed to create transaction" in str(exc_info.value)
    mock_repository.save.assert_called_once_with(create_transaction_data)


@pytest.mark.asyncio
async def test_create_transaction_with_generic_exception(
    mock_repository, create_transaction_data
):
    """Test transaction creation with generic exception."""
    # Arrange
    generic_error = ValueError("Database connection lost")
    mock_repository.save = AsyncMock(side_effect=generic_error)
    use_case = CreateTransactionUseCase(mock_repository)

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        await use_case.execute(create_transaction_data)

    assert "Failed to create transaction" in str(exc_info.value)
    mock_repository.save.assert_called_once_with(create_transaction_data)


@pytest.mark.asyncio
async def test_create_transaction_with_pending_status(
    mock_repository, mock_transaction_model
):
    """Test successful transaction creation with PENDING status."""
    # Arrange
    pending_data = TransactionCreate(
        amount=50.0,
        status=TransactionStatus.PENDING,
        account_id=2,
    )

    mock_transaction = Mock(spec=TransactionModel)
    mock_transaction.id = 2
    mock_transaction.amount = 50.0
    mock_transaction.status = "PENDING"
    mock_transaction.account = Mock(id=2, balance=500.0, type="savings")

    mock_repository.save = AsyncMock(return_value=mock_transaction)
    use_case = CreateTransactionUseCase(mock_repository)

    # Act
    result = await use_case.execute(pending_data)

    # Assert
    assert result.id == 2
    assert result.amount == 50.0
    assert result.status == TransactionStatus.PENDING


@pytest.mark.asyncio
async def test_create_transaction_with_zero_amount(
    mock_repository, mock_transaction_model
):
    """Test transaction creation with zero amount."""
    # Arrange
    zero_amount_data = TransactionCreate(
        amount=0.0,
        status=TransactionStatus.SUCCESS,
        account_id=1,
    )

    mock_transaction = Mock(spec=TransactionModel)
    mock_transaction.id = 3
    mock_transaction.amount = 0.0
    mock_transaction.status = "SUCCESS"
    mock_transaction.account = Mock(id=1, balance=1000.0, type="checking")

    mock_repository.save = AsyncMock(return_value=mock_transaction)
    use_case = CreateTransactionUseCase(mock_repository)

    # Act
    result = await use_case.execute(zero_amount_data)

    # Assert
    assert result.amount == 0.0


@pytest.mark.asyncio
async def test_create_transaction_with_large_amount(mock_repository):
    """Test transaction creation with large amount."""
    # Arrange
    large_amount_data = TransactionCreate(
        amount=999999.99,
        status=TransactionStatus.SUCCESS,
        account_id=1,
    )

    mock_transaction = Mock(spec=TransactionModel)
    mock_transaction.id = 4
    mock_transaction.amount = 999999.99
    mock_transaction.status = "SUCCESS"
    mock_transaction.account = Mock(id=1, balance=1000000.0, type="checking")

    mock_repository.save = AsyncMock(return_value=mock_transaction)
    use_case = CreateTransactionUseCase(mock_repository)

    # Act
    result = await use_case.execute(large_amount_data)

    # Assert
    assert result.amount == 999999.99


@pytest.mark.asyncio
async def test_create_transaction_response_structure(
    mock_repository, create_transaction_data, mock_transaction_model
):
    """Test that response has correct structure and all required fields."""
    # Arrange
    mock_repository.save = AsyncMock(return_value=mock_transaction_model)
    use_case = CreateTransactionUseCase(mock_repository)

    # Act
    result = await use_case.execute(create_transaction_data)

    # Assert - Check all attributes exist
    assert hasattr(result, "id")
    assert hasattr(result, "amount")
    assert hasattr(result, "status")
    assert hasattr(result, "account")

    assert hasattr(result.account, "id")
    assert hasattr(result.account, "balance")
    assert hasattr(result.account, "type")


@pytest.mark.asyncio
async def test_create_transaction_with_savings_account(mock_repository):
    """Test transaction creation with savings account type."""
    # Arrange
    transaction_data = TransactionCreate(
        amount=500.0,
        status=TransactionStatus.SUCCESS,
        account_id=5,
    )

    mock_transaction = Mock(spec=TransactionModel)
    mock_transaction.id = 5
    mock_transaction.amount = 500.0
    mock_transaction.status = "SUCCESS"
    mock_transaction.account = Mock(id=5, balance=5000.0, type="savings")

    mock_repository.save = AsyncMock(return_value=mock_transaction)
    use_case = CreateTransactionUseCase(mock_repository)

    # Act
    result = await use_case.execute(transaction_data)

    # Assert
    assert result.account.type == "savings"


@pytest.mark.asyncio
async def test_create_transaction_repository_called_with_correct_data(
    mock_repository, create_transaction_data
):
    """Test that repository.save is called with correct transaction data."""
    # Arrange
    mock_transaction = Mock(spec=TransactionModel)
    mock_transaction.id = 1
    mock_transaction.amount = create_transaction_data.amount
    mock_transaction.status = create_transaction_data.status.value
    mock_transaction.account = Mock(
        id=create_transaction_data.account_id, balance=1000.0, type="checking"
    )

    mock_repository.save = AsyncMock(return_value=mock_transaction)
    use_case = CreateTransactionUseCase(mock_repository)

    # Act
    await use_case.execute(create_transaction_data)

    # Assert
    mock_repository.save.assert_called_once()
    call_args = mock_repository.save.call_args[0][0]
    assert call_args.amount == create_transaction_data.amount
    assert call_args.status == create_transaction_data.status
    assert call_args.account_id == create_transaction_data.account_id
