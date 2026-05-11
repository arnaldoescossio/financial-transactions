from datetime import datetime, timezone
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from app.domain.enums.transaction_status import TransactionStatus

if TYPE_CHECKING:
    from app.domain.entities.account import Account


class Transaction(BaseModel):
    id: int | None = None
    amount: float | None = Field(ge=0.00)
    status: TransactionStatus | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    account: "Account | None" = None
    account_id: int | None = None

    @property
    def is_valid(self) -> bool:
        return self.status == TransactionStatus.SUCCESS and self.amount > 0

    @property
    def is_failed(self) -> bool:
        return self.status == TransactionStatus.FAILED
