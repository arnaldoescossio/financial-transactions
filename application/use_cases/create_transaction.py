
from application.config.logging_config import logger

from domain.repositories.transaction_repository import TransactionRepository
from application.dtos.create_transaction_dto import CreateTransactionDTO


class CreateTransactionUseCase:
    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    def execute(self, data: CreateTransactionDTO) -> CreateTransactionDTO:
        transaction = self.repository.save(data.to_entity())
        logger.info(f"Transaction {transaction.id} created successfully")

        return CreateTransactionDTO.from_entity(transaction)