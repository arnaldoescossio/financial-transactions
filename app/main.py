from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.exception_handler.handlers import register_exception_handlers
from app.api.v1.routes.accounts_api import router as account_router
from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.admin_api import router as admin_router
from app.api.v1.routes.transactions_api import router as transaction_router
from app.core.config.env_config import settings
from app.core.config.logging_config import logger
from app.infrastructure.database import engine


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # ── Startup ──────────────────────────────────────────────────────────
    logger.info("Application starting up...")
    yield
    # ── Shutdown ─────────────────────────────────────────────────────────
    logger.info("Application shutting down...")
    await engine.dispose()


app = FastAPI(root_path="/api/v1", lifespan=lifespan)

# ── CORS ─────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(auth_router, prefix="/token")
app.include_router(transaction_router, prefix="/transactions")
app.include_router(account_router, prefix="/accounts")
app.include_router(admin_router, prefix="/admin")

