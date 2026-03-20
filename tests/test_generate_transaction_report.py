import pytest

from application.use_cases.transaction.generate_transaction_report import GenerateTransactionReportUseCase
from domain.entities.transaction import Transaction
from domain.enums.transaction_status import TransactionStatus
from domain.repositories.transaction_repository import TransactionRepository

def test_generate_transaction_report():
    class FakeTransactionRepository(TransactionRepository):
        def get_all(self):
            return [
                # Valid transaction
                Transaction(id=1, amount=100.0, status=TransactionStatus.SUCCESS),
                # Failed transaction
                Transaction(id=2, amount=50.0, status=TransactionStatus.FAILED),
                # Another valid transaction         
                Transaction(id=3, amount=200.0, status=TransactionStatus.SUCCESS),
            ]

        def save(self, transaction):
            raise None

        
    repository = FakeTransactionRepository()
    use_case = GenerateTransactionReportUseCase(repository)

    report = use_case.execute()

    assert report.valid_count == 2
    assert report.total_amount == 300.0
    assert report.average_amount == 150.0
    assert report.failed_count == 1 

def test_generate_transaction_report_no_valid_transactions():
    class EmptyTransactionRepository(TransactionRepository):
        def get_all(self):
            return [
                Transaction(id=1, amount=100.0, status=TransactionStatus.FAILED),
                Transaction(id=2, amount=50.0, status=TransactionStatus.FAILED),
                Transaction(id=3, amount=0.0, status=TransactionStatus.SUCCESS),
            ]

        def save(self, transaction):
            return None


    repository = EmptyTransactionRepository()
    use_case = GenerateTransactionReportUseCase(repository)

    with pytest.raises(Exception) as exc_info:
        use_case.execute()

    assert str(exc_info.value) == "No valid transactions found."