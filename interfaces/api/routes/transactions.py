from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from application.use_cases.generate_transaction_report import GenerateTransactionReportUseCase
from domain.exceptions.no_valid_transactions_exception import NoValidTransactionException
from infrastructure.repositories.postgres_transaction_repository import PostgresTransactionRepository
from infrastructure.database import get_db
from application.config.logging_config import logger
from interfaces.api.security.security import verify_token

app = FastAPI()

def get_use_case(db: Session = Depends(get_db)):
    repository = PostgresTransactionRepository(db)
    use_case = GenerateTransactionReportUseCase(repository)
    return use_case

@app.get("/transactions/report")
def generate_report(
    user = Depends(verify_token),
    use_case: GenerateTransactionReportUseCase = Depends(get_use_case)
):
    try:
        logger.info(f"User {user['user']} is generating a transaction report")
        return use_case.execute()
    except NoValidTransactionException as e:
        logger.error(f"Error: {e}")
        return {"error": str(e)}
  