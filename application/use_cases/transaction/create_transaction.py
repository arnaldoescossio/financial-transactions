
from typing import override

from application.config.logging_config import logger

from application.dtos.base_dto import Dto
from application.use_cases.base_use_case import UseCase
from domain.repositories.transaction_repository import TransactionRepository
from application.dtos.create_transaction_dto import CreateTransactionDTO


class CreateTransactionUseCase(UseCase[CreateTransactionDTO]):
    
    @override
    def execute(self, data: CreateTransactionDTO) -> CreateTransactionDTO:
        transaction = self.repository.save(data.to_entity())
        logger.info(f"Transaction {transaction.id} created successfully")

        return CreateTransactionDTO.from_entity(transaction)