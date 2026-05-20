from pydantic import BaseModel, ConfigDict

from app.api.v1.schemas.account_schema import AccountBase
from app.domain.enums.transaction_status import TransactionStatus


class TransactionBase(BaseModel):
    id: int | None = None
    amount: float
    status: TransactionStatus


class TransactionCreate(TransactionBase):
    account_id: int


class TransactionResponse(TransactionBase):
    model_config = ConfigDict(from_attributes=True)

    account: AccountBase | None = None
