from dataclasses import dataclass
from domain.enums.transaction_status import TransactionStatus

@dataclass
class Transaction:
    id: int
    amount: float
    status: TransactionStatus
    # account_id: int 

    def is_valid(self) -> bool:
        return self.status == TransactionStatus.SUCCESS and self.amount > 0
    
    def is_failed(self) -> bool:
        return self.status == TransactionStatus.FAILED