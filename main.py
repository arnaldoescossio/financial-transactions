from contextlib import asynccontextmanager

from starlette import status
from starlette.responses import JSONResponse
import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.routes.accounts_api import router as account_router
from api.routes.auth import router as auth_router
from api.routes.transactions_api import router as transaction_router
from application.config.logging_config import logger
from domain.exceptions.account_not_found import AccountNotFoundException
from domain.exceptions.no_valid_transactions_exception import (
    NoValidTransactionException,
)
from infrastructure.database import Base, engine


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # ── Startup ──────────────────────────────────────────────────────────
    logger.info("Application starting up...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # ── Shutdown ─────────────────────────────────────────────────────────
    logger.info("Application shutting down...")
    await engine.dispose()


app = FastAPI(root_path="/api/v1", lifespan=lifespan)

app.include_router(auth_router, prefix="/token")
app.include_router(transaction_router, prefix="/transactions")
app.include_router(account_router, prefix="/accounts")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)

@app.exception_handler(StarletteHTTPException)
async def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )
    return JSONResponse(
        status_code=exception.status_code,
        content={"detail": message},
    )

@app.exception_handler(RequestValidationError)
async def general_http_exception_handler(request: Request, exception: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": exception.errors()},
    )

@app.exception_handler(NoValidTransactionException)
async def general_http_exception_handler(request: Request, exception: NoValidTransactionException):
    return not_found(exception)

@app.exception_handler(AccountNotFoundException)
async def general_http_exception_handler(request: Request, exception: AccountNotFoundException):
    return not_found(exception)

@app.exception_handler(Exception)
async def general_http_exception_handler(request: Request, exception: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred."},
    )

def not_found(exception):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,  
        content={"detail": exception.args[0]},
    )
