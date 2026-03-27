from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from application.use_cases.transaction.create_transaction import CreateTransactionUseCase
from application.use_cases.transaction.get_transactions_by_account import GetTransactionsByAccountUseCase
from domain.entities.transaction import TransactionCreate, TransactionResponse
from domain.enums.transaction_status import TransactionStatus
from domain.repositories.transaction_repository import TransactionRepository
from infrastructure.database import get_db
from application.config.logging_config import logger
from api.security.auth import verify_token

router = APIRouter(prefix="/api/v1", tags=["transactions"])


@router.post(
    "/transactions",
    response_model=TransactionResponse,
    response_model_exclude={"transactions"},
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    transaction_data: TransactionCreate,
    user = Depends(verify_token),
    db: Session = Depends(get_db)
) -> TransactionResponse:
    logger.info(f"User {user['user']} is creating a new transaction")
    repository = TransactionRepository(db)
    use_case = CreateTransactionUseCase(repository)
    return use_case.execute(transaction_data)

@router.get(
    "/transactions/{account_id}/accounts",
    response_model=list[TransactionResponse],
    response_model_exclude={
        "__all__": {
            "account"
        }
    }
)
def list_transactions(
    account_id: int,
    status: dict[str, TransactionStatus],
    user = Depends(verify_token),
    db: Session = Depends(get_db)
) -> list[TransactionResponse]:
    logger.info(f"User {user['user']} is requesting transactions for account {account_id} with status {status['status']}")
    repository = TransactionRepository(db)
    use_case = GetTransactionsByAccountUseCase(repository)
    return use_case.execute(account_id, status['status'])  


    # except NoValidTransactionException as e:
    #     logger.error(f"Error: {e}")
    #     raise HTTPException(
    #         status_code=400,
    #         detail={"error": str(e)}
    #     )
    # except Exception as e:
    #     logger.error(f"Error generating report: {e}")
    #     raise HTTPException(
    #         status_code=400,
    #         detail={"error": str(e)}
    #     )
