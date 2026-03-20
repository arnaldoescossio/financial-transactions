import pytest
from unittest.mock import Mock

from pytest_mock import mocker

from application.use_cases.transaction.create_transaction import CreateTransactionUseCase
from application.dtos.create_transaction_dto import CreateTransactionDTO
from domain.entities.transaction import Transaction
from domain.enums.transaction_status import TransactionStatus
from domain.repositories.transaction_repository import TransactionRepository


class FakeTransactionRepository(TransactionRepository):
    """Fake repository for testing."""
    def __init__(self):
        self.saved_transactions = []

    def save(self, transaction: Transaction) -> Transaction:
        transaction.id = len(self.saved_transactions) + 1
        self.saved_transactions.append(transaction)
        return transaction

    def get_all(self):
        return self.saved_transactions


def test_create_transaction_use_case_execute(mocker):
    """Test successful transaction creation."""
    repository = FakeTransactionRepository()
    use_case = CreateTransactionUseCase(repository)

    # Create DTO
    dto = CreateTransactionDTO(amount=100.0, status="SUCCESS")
    
    # Mock the to_entity method
    mock_transaction = Transaction(id=None, amount=100.0, status=TransactionStatus.SUCCESS)
    mocker.patch.object(dto, "to_entity", return_value=mock_transaction)
    dto.to_entity = Mock(return_value=mock_transaction)
    
    # Execute
    result = use_case.execute(dto)

    # Verify
    assert result is not None
    assert isinstance(result, CreateTransactionDTO)
    dto.to_entity.assert_called_once()


def test_create_transaction_use_case_saves_to_repository():
    """Test that transaction is saved to repository."""
    repository = FakeTransactionRepository()
    use_case = CreateTransactionUseCase(repository)

    # Create a real transaction
    transaction = Transaction(id=None, amount=50.0, status=TransactionStatus.SUCCESS)
    dto = CreateTransactionDTO(amount=50.0, status="SUCCESS")
    dto.to_entity = Mock(return_value=transaction)
    
    # Execute
    result = use_case.execute(dto)

    # Verify repository was called
    assert len(repository.saved_transactions) == 1
    assert repository.saved_transactions[0].amount == 50.0


def test_create_transaction_use_case_with_mock_repository():
    """Test with mocked repository."""
    # Create mock repository
    mock_repository = Mock(spec=TransactionRepository)
    mock_transaction = Transaction(id=1, amount=75.0, status=TransactionStatus.SUCCESS)
    mock_repository.save.return_value = mock_transaction

    use_case = CreateTransactionUseCase(mock_repository)

    dto = CreateTransactionDTO(amount=75.0, status="SUCCESS")
    dto.to_entity = Mock(return_value=mock_transaction)
    
    result = use_case.execute(dto)

    # Verify repository was called
    mock_repository.save.assert_called_once()
