from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar
from domain.entities.account import AccountResponse
from domain.enums.transaction_status import TransactionStatus
from pydantic import BaseModel, ConfigDict, Field, field_validator

class Transaction(BaseModel):
    amount: float
    status: TransactionStatus

    def is_valid(self) -> bool:
        return self.status == TransactionStatus.SUCCESS and self.amount > 0
    
    def is_failed(self) -> bool:
        return self.status == TransactionStatus.FAILED
    
class TransactionCreate(Transaction):
    account_id: int

class TransactionResponse(Transaction):
    model_config = ConfigDict(from_attributes=True)

    id: int
    account : AccountResponse | None = None