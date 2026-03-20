from typing import override

from application.config.logging_config import logger
from application.dtos.transaction_report_dto import TransactionReportDTO

from application.use_cases.base_use_case import UseCase
from domain.exceptions.no_valid_transactions_exception import NoValidTransactionException
from domain.repositories.transaction_repository import TransactionRepository


class GenerateTransactionReportUseCase(UseCase[TransactionReportDTO]):      

    @override
    def execute(self) -> TransactionReportDTO: 

        transactions = self.repository.get_all()

        valid_transactions = [t for t in transactions if t.is_valid()]

        if not valid_transactions:
            raise NoValidTransactionException("No valid transactions found.")

        total_amount: float = sum(t.amount for t in valid_transactions)
        valid_count: int = sum(1 for t in valid_transactions)
        average_amount: float = total_amount / valid_count if valid_count > 0 else 0
        failed_count: int = sum(1 for t in transactions if t.is_failed())

        logger.info(
            "Transaction report generated successfully.",
            valid_count=valid_count,
            total_amount=total_amount,
            average_amount=average_amount,
            failed_count=failed_count
        )

        return TransactionReportDTO(
            valid_count, total_amount, average_amount, failed_count
        )
