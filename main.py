from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.exception_handler.handlers import register_exception_handlers
from api.routes.accounts_api import router as account_router
from api.routes.auth import router as auth_router
from api.routes.transactions_api import router as transaction_router
from application.config.logging_config import logger
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

register_exception_handlers(app)

app.include_router(auth_router, prefix="/token")
app.include_router(transaction_router, prefix="/transactions")
app.include_router(account_router, prefix="/accounts")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)