from decimal import Decimal

from domain.entities.transaction import Transaction
from pydantic import BaseModel, ConfigDict, Field, field_validator

class Account(BaseModel):
    id: int | None 
    balance: float = 0.00
    transactions: list[Transaction] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

    @field_validator("balance")
    @classmethod
    def balance_non_negative(cls, value: float) -> float:
        if value < 0.00:
            raise ValueError("balance cannot be negative")
        return value

# Todas as classes abaixo serão usadas para validação e transferência de dados, mas não possuem lógica de negócios complexa,

class AccountCreate(BaseModel):
    balance: float

class AccountRead(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    id: int 
    balance: float
    transactions: list[Transaction] = []

# AccountUpdate can be used for partial updates, so all fields are optional
# class AccountUpdate(BaseModel):
#     balance: Decimal | None = None

#     @field_validator("balance")
#     @classmethod
#     def balance_non_negative(cls, v: Decimal | None) -> Decimal | None:
#         if v is not None and v < Decimal("0.00"):
#             raise ValueError("balance cannot be negative")
#         return v.quantize(Decimal("0.01")) if v is not None else None

## 
# I removed the dataclass version of Account since we're using Pydantic models for validation and serialization. 
# The AccountRead model can be used to represent the account data when reading from the database, 
#   while AccountCreate and AccountUpdate can be used for creating and updating accounts, respectively.
##

    # def add_transaction(self, transaction: Transaction):
    #     transaction.account_id = self.id
    #     self.transactions.append(transaction)
    #     self.balance += transaction.amount

    # def get_transaction_by_status(self, status: TransactionStatus) -> list[Transaction]:
    #     return [t for t in self.transactions if t.status == status]
