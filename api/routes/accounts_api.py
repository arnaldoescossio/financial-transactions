from typing import Annotated, Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.security.auth import verify_token
from application.config.logging_config import logger
from application.use_cases.account.create_account import CreateAccountUseCase
from application.use_cases.account.get_account import GetAccountUseCase
from domain.entities.account import AccountCreate, AccountResponse
from domain.repositories.account_repository import AccountRepository
from infrastructure.database import get_db

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
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AccountResponse:
    logger.info(f"User {user['user']} is creating a new account")
    use_case = CreateAccountUseCase(repository=AccountRepository(db))
    return await use_case.execute(account_data)


@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(
    account_id: int,
    user: Annotated[dict[str, Any], Depends(verify_token)],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> AccountResponse:
    logger.info(f"User {user['user']} is requesting details of account {account_id}")
    use_case = GetAccountUseCase(repository=AccountRepository(db))
    return await use_case.execute(account_id)
