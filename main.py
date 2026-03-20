
import uvicorn
from fastapi import FastAPI
from interfaces.api.routes.accounts import router as account_router
from interfaces.api.routes.auth import router as auth_router
from interfaces.api.routes.transactions import router as transaction_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(transaction_router)
app.include_router(account_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)