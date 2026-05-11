from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from app.api.security.auth import verify_token
from app.api.v1.schemas.account_schema import AccountCreate, AccountResponse
from app.core.config.logging_config import logger
from app.core.factories.use_cases.create_account_use_case_factory import (
    get_create_account_use_case,
)
from app.core.factories.use_cases.find_account_use_case_factory import (
    get_find_account_use_case,
)
from app.use_cases.account.create_account import CreateAccountUseCase
from app.use_cases.account.find_account import FindAccountUseCase

router = APIRouter(tags=["accounts"])


@router.post(
    "",
    response_model=AccountResponse,
    response_model_exclude={"transactions"},
    status_code=status.HTTP_201_CREATED,
)
async def create_account(
    account_data: AccountCreate,
    user: Annotated[dict[str, Any], Depends(verify_token)],
    use_case: Annotated[CreateAccountUseCase, Depends(get_create_account_use_case)],
) -> AccountResponse:
    logger.info(f"User {user['user']} is creating a new account")

    return await use_case.execute(account_data)


@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(
    account_id: int,
    user: Annotated[dict[str, Any], Depends(verify_token)],
    use_case: Annotated[FindAccountUseCase, Depends(get_find_account_use_case)],
) -> AccountResponse:
    logger.info(f"User {user['user']} is requesting details of account {account_id}")
    return await use_case.execute(account_id)
