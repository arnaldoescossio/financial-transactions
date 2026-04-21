from typing import Annotated, Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.security.auth import verify_token
from application.config.logging_config import logger
from application.use_cases.transaction.create_transaction import \
    CreateTransactionUseCase
from application.use_cases.transaction.get_transactions_by_account import \
    GetTransactionsByAccountUseCase
from domain.entities.transaction import TransactionCreate, TransactionResponse
from domain.enums.transaction_status import TransactionStatus
from domain.repositories.transaction_repository import TransactionRepository
from infrastructure.database import get_db

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
    response_model_exclude={
        "__all__": {
            "account"
        }
    }
)
async def list_transactions(
    account_id: int,
    status: dict[str, TransactionStatus],
    user: Annotated[dict[str, Any], Depends(verify_token)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[TransactionResponse]:
    logger.info(f"User {user['user']} is requesting transactions for account {account_id} with status {status['status']}")
    repository = TransactionRepository(db)
    use_case = GetTransactionsByAccountUseCase(repository)
    return await use_case.execute(account_id, status['status'])  