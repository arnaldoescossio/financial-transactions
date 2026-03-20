from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from application.config.logging_config import logger
from application.dtos.create_account_dto import CreateAccountDTO
from application.use_cases.account.create_account import CreateAccountUseCase
from domain.entities.account import Account, AccountCreate, AccountRead, AccountRead
from domain.repositories.account_repository import AccountRepository
from infrastructure.database import get_db
from interfaces.api.security.security import verify_token


router = APIRouter(prefix="/api/v1", tags=["accounts"])

@router.post("/accounts")
def create_account(
    account_data: AccountCreate,
    user = Depends(verify_token),
    db: Session = Depends(get_db)
) -> AccountRead:
    logger.info(f"User {user['user']} is creating a new account")
    use_case = CreateAccountUseCase(repository=AccountRepository(db))
    dto = use_case.execute(CreateAccountDTO.from_entity(account_data))
    return AccountRead(
        id=dto.id,
        balance=dto.balance
    )
    # return dto.to_entity()

# @router.get("/accounts")
# def get_accounts():
#     logger.info("User is requesting the list of accounts")
#     return {"message": "List of accounts"}

# @router.get("/account/{account_id}")
# def get_account(account_id: int):
#     logger.info(f"User is requesting details of account {account_id}")
#     return {"message": f"Details of account {account_id}"}