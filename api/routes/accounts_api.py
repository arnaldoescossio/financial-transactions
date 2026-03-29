from fastapi import APIRouter, status, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from application.config.logging_config import logger
from application.use_cases.account.create_account import CreateAccountUseCase
from application.use_cases.account.get_account import GetAccountUseCase
from domain.entities.account import AccountCreate, AccountResponse
from domain.repositories.account_repository import AccountRepository
from infrastructure.database import get_db
from api.security.auth import verify_token


router = APIRouter(tags=["accounts"])


@router.post(
    "",
    response_model=AccountResponse,
    response_model_exclude={"transactions"},
    status_code=status.HTTP_201_CREATED,
)
def create_account(
    account_data: AccountCreate,
    user=Depends(verify_token),
    db: Session = Depends(get_db),
) -> AccountResponse:
    logger.info(f"User {user['user']} is creating a new account")
    use_case = CreateAccountUseCase(repository=AccountRepository(db))
    return use_case.execute(account_data)

@router.get("/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: int,
    user = Depends(verify_token),
    db: Session = Depends(get_db)
) -> AccountResponse:
    logger.info(f"User {user['user']} is requesting details of account {account_id}")
    use_case = GetAccountUseCase(repository=AccountRepository(db))
    return use_case.execute(account_id)
