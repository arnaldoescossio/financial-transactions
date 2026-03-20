import pytest
from unittest.mock import Mock

from application.use_cases.use_case_factory import UseCaseFactory
from application.use_cases.transaction.create_transaction import CreateTransactionUseCase
from application.use_cases.transaction.generate_transaction_report import GenerateTransactionReportUseCase
from application.use_cases.enums.transaction_use_case_type import TransactionUseCaseType
from domain.repositories.transaction_repository import TransactionRepository


def test_factory_create_create_transaction_use_case():
    """Test factory creates CreateTransactionUseCase correctly."""
    mock_repository = Mock(spec=TransactionRepository)
    
    use_case = UseCaseFactory.create(
        TransactionUseCaseType.CREATE, 
        mock_repository
    )

    assert isinstance(use_case, CreateTransactionUseCase)
    assert use_case.repository == mock_repository


def test_factory_create_generate_report_use_case():
    """Test factory creates GenerateTransactionReportUseCase correctly."""
    mock_repository = Mock(spec=TransactionRepository)
    
    use_case = UseCaseFactory.create(
        TransactionUseCaseType.REPORT, 
        mock_repository
    )

    assert isinstance(use_case, GenerateTransactionReportUseCase)
    assert use_case._repository == mock_repository


def test_factory_with_invalid_use_case_type():
    """Test factory raises error with invalid use case type."""
    mock_repository = Mock(spec=TransactionRepository)
    
    with pytest.raises(ValueError) as exc_info:
        UseCaseFactory.create("invalid_type", mock_repository)
    
    assert "Invalid use case type" in str(exc_info.value)


def test_factory_enum_has_use_case_class():
    """Test that enum values have use_case_class attribute."""
    assert hasattr(TransactionUseCaseType.CREATE, 'use_case_class')
    assert hasattr(TransactionUseCaseType.REPORT, 'use_case_class')
    assert TransactionUseCaseType.CREATE.use_case_class == CreateTransactionUseCase
    assert TransactionUseCaseType.REPORT.use_case_class == GenerateTransactionReportUseCase


def test_factory_enum_has_slug():
    """Test that enum values have slug attribute."""
    assert hasattr(TransactionUseCaseType.CREATE, 'slug')
    assert hasattr(TransactionUseCaseType.REPORT, 'slug')
    assert TransactionUseCaseType.CREATE.slug == "create"
    assert TransactionUseCaseType.REPORT.slug == "report"
