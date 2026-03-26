from domain.entities.account import AccountBase
from domain.enums.transaction_status import TransactionStatus
from pydantic import BaseModel, ConfigDict

class TransactionBase(BaseModel):
    id: int | None = None
    amount: float
    status: TransactionStatus

    def is_valid(self) -> bool:
        return self.status == TransactionStatus.SUCCESS and self.amount > 0
    
    def is_failed(self) -> bool:
        return self.status == TransactionStatus.FAILED
    
class TransactionCreate(TransactionBase):
    account_id: int

class TransactionResponse(TransactionBase):
    model_config = ConfigDict(from_attributes=True)

    account : AccountBase | None = None