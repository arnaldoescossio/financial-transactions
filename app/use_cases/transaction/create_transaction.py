from typing import override

from asyncpg import exceptions
from sqlalchemy.exc import IntegrityError

from app.core.config.logging_config import logger
from app.api.v1.schemas.account_schema import AccountResponse
from app.api.v1.schemas.transaction_schema import TransactionCreate, TransactionResponse
from app.domain.exceptions.account_not_found import AccountNotFoundException
from app.infrastructure.adapters.repositories.transaction_repository import TransactionRepository
from app.use_cases.base_use_case import UseCase


class CreateTransactionUseCase(UseCase[TransactionCreate, TransactionCreate, TransactionRepository]):
    """Use case for creating a new transaction."""
    @override
    async def execute(self, data: TransactionCreate) -> TransactionResponse:
        try:
            transaction = await self.repository.save(data)
            logger.info(f"Transaction {transaction.id} created successfully")
        except IntegrityError as e:
            if isinstance(e.orig.__cause__, exceptions.ForeignKeyViolationError):
                logger.error(f"Foreign key violation: {e}")
                raise AccountNotFoundException(
                    "Failed to create transaction: Account not found"
                )
            else:
                logger.error(f"Integrity error: {e}")
                raise Exception("Failed to create transaction")
        except Exception as e:
            logger.error(f"Error occurred while creating transaction: {e}")
            raise Exception("Failed to create transaction")

        return TransactionResponse(
            id=transaction.id,
            amount=transaction.amount,
            status=transaction.status,
            account=AccountResponse(
                id=transaction.account.id,
                balance=transaction.account.balance,
                type=transaction.account.type,
            ),
        )
