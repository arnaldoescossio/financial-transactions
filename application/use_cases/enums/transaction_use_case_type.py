
from enum import Enum

from application.use_cases.base_use_case import UseCase
from application.use_cases.create_transaction import CreateTransactionUseCase
from application.use_cases.generate_transaction_report import GenerateTransactionReportUseCase


class TransactionUseCaseType(Enum):
    CREATE = "create", CreateTransactionUseCase
    REPORT = "report", GenerateTransactionReportUseCase

    def __init__(self, slug: str, use_case_class):    
        self.slug = slug
        self.use_case_class = use_case_class