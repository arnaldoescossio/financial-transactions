from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator


class AccountBase(BaseModel):
    id: int | None = None
    balance: float = Field(ge=0.00)
    type: Literal["checking", "savings"] = Field(default="checking")

    # @field_validator("balance")
    # @classmethod
    # def balance_non_negative(cls, value: float) -> float:
    #     if value < 0.00:
    #         raise ValueError("balance cannot be negative")
    #     return value

class AccountCreate(AccountBase):
    pass

class AccountResponse(AccountBase):
    model_config = ConfigDict(from_attributes=True)

    transactions: list | None = None


#     @field_validator("balance")
#     @classmethod
#     def balance_non_negative(cls, v: Decimal | None) -> Decimal | None:
#         if v is not None and v < Decimal("0.00"):
#             raise ValueError("balance cannot be negative")
#         return v.quantize(Decimal("0.01")) if v is not None else None

    # def add_transaction(self, transaction: Transaction):
    #     transaction.account_id = self.id
    #     self.transactions.append(transaction)
    #     self.balance += transaction.amount

    # def get_transaction_by_status(self, status: TransactionStatus) -> list[Transaction]:
    #     return [t for t in self.transactions if t.status == status]
