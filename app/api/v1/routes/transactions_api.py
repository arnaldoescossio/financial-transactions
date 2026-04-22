from typing import Annotated, Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.security.auth import verify_token
from app.config.logging_config import logger
from app.domain.entities.transaction import TransactionCreate, TransactionResponse
from app.domain.enums.transaction_status import TransactionStatus
from app.domain.repositories.transaction_repository import TransactionRepository
from app.infrastructure.database import get_db
from app.use_cases.transaction.create_transaction import CreateTransactionUseCase
from app.use_cases.transaction.get_transactions_by_account import (
    GetTransactionsByAccountUseCase,
)

router = APIRouter(tags=["transactions"])


@router.post(
    "",
    response_model=TransactionResponse,
    response_model_exclude={"transactions"},
    status_code=status.HTTP_201_CREATED,
)
async def create_transaction(
    transaction_data: TransactionCreate,
    user: Annotated[dict[str, Any], Depends(verify_token)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TransactionResponse:
    logger.info(f"User {user['user']} is creating a new transaction")
    repository = TransactionRepository(db)
    use_case = CreateTransactionUseCase(repository)
    return await use_case.execute(transaction_data)


@router.get(
    "/{account_id}/account",
    response_model=list[TransactionResponse],
    response_model_exclude={"__all__": {"account"}},
)
async def list_transactions(
    account_id: int,
    status: dict[str, TransactionStatus],
    user: Annotated[dict[str, Any], Depends(verify_token)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[TransactionResponse]:
    logger.info(
        f"User {user['user']} is requesting transactions for account {account_id} with status {status['status']}"
    )
    repository = TransactionRepository(db)
    use_case = GetTransactionsByAccountUseCase(repository)
    return await use_case.execute(account_id, status["status"])
