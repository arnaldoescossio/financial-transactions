from datetime import datetime, timezone
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from app.domain.entities.transaction import Transaction


class Account(BaseModel):
    id: int | None = None
    balance: float | None = None
    type: Literal["checking", "savings"] = Field(default="checking")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    transactions: list["Transaction"] | None = None

    # def add_transaction(self, transaction: "Transaction") -> None:
    #     transaction.account_id = self.id
    #     if self.transactions is None:
    #         self.transactions = []
    #     self.transactions.append(transaction)
    #     self.balance += transaction.amount

    # def get_transaction_by_status(
    #     self, status: TransactionStatus
    # ) -> list["Transaction"]:
    #     if self.transactions is None:
    #         return []
    #     return [t for t in self.transactions if t.status == status]
