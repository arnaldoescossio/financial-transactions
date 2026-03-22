from fastapi import APIRouter, status, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from application.config.logging_config import logger
from application.use_cases.account.create_account import CreateAccountUseCase
from domain.entities.account import AccountCreate, AccountResponse
from domain.repositories.account_repository import AccountRepository
from infrastructure.database import get_db
from api.security.auth import verify_token
from infrastructure.models.account_model import AccountModel


router = APIRouter(prefix="/api/v1", tags=["accounts"])

@router.post("/accounts", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(
    account_data: AccountCreate,
    user = Depends(verify_token),
    db: Session = Depends(get_db)
) -> AccountResponse:
    logger.info(f"User {user['user']} is creating a new account")
    use_case = CreateAccountUseCase(repository=AccountRepository(db))
    return use_case.execute(account_data)

@router.get("/accounts", response_model=list[AccountResponse])
def get_accounts(
    user = Depends(verify_token),
    db: Session = Depends(get_db)
) -> list[AccountResponse]:
    logger.info(f"User {user['user']} is requesting the list of accounts")
    accounts = db.execute(select(AccountModel)).scalars().all()
    return accounts

@router.get("/account/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: int,
    user = Depends(verify_token),
    db: Session = Depends(get_db)
) -> AccountResponse:
    logger.info(f"User is requesting details of account {account_id}")
    account = db.execute(select(AccountModel).where(AccountModel.id == account_id)).scalars().first()
    return account
