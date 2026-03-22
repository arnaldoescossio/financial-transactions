
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn
from fastapi import FastAPI, Request, status
from starlette.exceptions import HTTPException as StarletteHTTPException
from api.routes.accounts_api import router as account_router
from api.routes.auth import router as auth_router
from api.routes.transactions_api import router as transaction_router
from domain.exceptions.no_valid_transactions_exception import NoValidTransactionException

app = FastAPI()

app.include_router(auth_router)
app.include_router(transaction_router)
app.include_router(account_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)

@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
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
def general_http_exception_handler(request: Request, exception: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": exception.errors()},
    )

@app.exception_handler(NoValidTransactionException)
def general_http_exception_handler(request: Request, exception: NoValidTransactionException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,  
        content={"detail": exception.args[0]},
    )

@app.exception_handler(Exception)
def general_http_exception_handler(request: Request, exception: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred."},
    )
