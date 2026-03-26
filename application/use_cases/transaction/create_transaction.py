from typing import override
from psycopg2 import errors
from sqlalchemy.exc import IntegrityError

from application.config.logging_config import logger

from application.use_cases.base_use_case import UseCase
from domain.entities.account import AccountResponse
from domain.entities.transaction import TransactionCreate, TransactionResponse
from domain.exceptions.account_not_found import AccountNotFoundException


class CreateTransactionUseCase(UseCase[TransactionCreate]):
    
    @override
    def execute(self, data: TransactionCreate) -> TransactionResponse:
        try:
            transaction = self.repository.save(data)
            logger.info(f"Transaction {transaction.id} created successfully")
        except IntegrityError as e:
            if isinstance(e.orig, errors.ForeignKeyViolation):
                logger.error(f"Foreign key violation: {e}")
                raise AccountNotFoundException("Failed to create transaction: Account not found")
        except Exception as e:
            logger.error(f"Error occurred while creating transaction: {e}")
            raise AccountNotFoundException("Failed to create transaction")

        return TransactionResponse(
            id=transaction.id,
            amount=transaction.amount,
            status=transaction.status,
            account=AccountResponse(
                id=transaction.account.id,
                balance=transaction.account.balance,
                type=transaction.account.type
            )
        )