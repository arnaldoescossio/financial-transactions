from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from app.api.security.auth import verify_token
from app.api.v1.schemas.transaction_schema import TransactionCreate, TransactionResponse
from app.core.config.logging_config import logger
from app.core.factories.use_cases.create_transaction_use_case_factory import (
    get_create_transaction_use_case,
)
from app.core.factories.use_cases.get_transactions_by_account_use_case_factory import (
    get_get_transactions_by_account_use_case,
)
from app.domain.enums.transaction_status import TransactionStatus
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
    use_case: Annotated[
        CreateTransactionUseCase, Depends(get_create_transaction_use_case)
    ],
) -> TransactionResponse:
    logger.info(f"User {user['user']} is creating a new transaction")
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
    use_case: Annotated[
        GetTransactionsByAccountUseCase,
        Depends(get_get_transactions_by_account_use_case),
    ],
) -> list[TransactionResponse]:
    logger.info(
        f"User {user['user']} is requesting transactions for account {account_id} with status {status['status'].value}"
    )
    return await use_case.execute(dict(account_id=account_id, transaction_status=status['status']))
