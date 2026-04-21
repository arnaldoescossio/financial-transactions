from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from domain.exceptions.account_not_found import AccountNotFoundException
from domain.exceptions.no_valid_transactions_exception import (
    NoValidTransactionException,
)


def register_exception_handlers(app: FastAPI):
    
    @app.exception_handler(StarletteHTTPException)
    async def general_http_exception_handler(
        request: Request, exception: StarletteHTTPException
    ) -> JSONResponse:
        message = (
            exception.detail
            if exception.detail
            else "An error occurred while processing the request."
        )
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )

    @app.exception_handler(RequestValidationError)
    async def general_http_exception_handler(
        request: Request, exception: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )

    @app.exception_handler(NoValidTransactionException)
    async def general_http_exception_handler(
        request: Request, exception: NoValidTransactionException
    ) -> JSONResponse:
        return not_found(exception)

    @app.exception_handler(AccountNotFoundException)
    async def general_http_exception_handler(
        request: Request, exception: AccountNotFoundException
    ) -> JSONResponse:
        return not_found(exception)

    @app.exception_handler(Exception)
    async def general_http_exception_handler(request: Request, exception: Exception):
        return JSONResponse

    def not_found(exception):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exception.args[0]},
        )
