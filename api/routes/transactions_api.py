from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from application.use_cases.use_case_factory import UseCaseFactory
from application.dtos.create_transaction_dto import CreateTransactionDTO
from domain.exceptions.no_valid_transactions_exception import NoValidTransactionException
from domain.repositories.transaction_repository import TransactionRepository
from infrastructure.database import get_db
from application.config.logging_config import logger
from application.use_cases.enums.transaction_use_case_type import TransactionUseCaseType
from api.security.auth import verify_token

router = APIRouter(prefix="/api/v1", tags=["transactions"])

@router.post("/transactions")
def create_transaction(
    transaction_data: CreateTransactionDTO,
    user = Depends(verify_token),
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"User {user['user']} is creating a new transaction")
        repository = TransactionRepository(db)
        use_case = UseCaseFactory.create(TransactionUseCaseType.CREATE, repository)
        return use_case.execute(transaction_data)
    except Exception as e:
        logger.error(f"Error creating transaction: {e}")
        raise HTTPException(
            status_code=400,
            detail={"error": str(e)}
        )

@router.get("/transactions/report")
def generate_report(
    user = Depends(verify_token),
    db: Session = Depends(get_db)
):
    # try:
    logger.info(f"User {user['user']} is generating a transaction report")
    repository = TransactionRepository(db)
    use_case = UseCaseFactory.create(TransactionUseCaseType.REPORT, repository)
    return use_case.execute()
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
        