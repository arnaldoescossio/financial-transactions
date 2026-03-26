from typing import override

from application.use_cases.base_use_case import UseCase

from application.config.logging_config import logger
from domain.entities.transaction import TransactionBase
from domain.enums.transaction_status import TransactionStatus

class GetTransactionsByAccountUseCase(UseCase):

    @override
    def execute(self, account_id: int, transaction_status: TransactionStatus = TransactionStatus.SUCCESS) -> list[TransactionBase]:
        transactions = self.repository.get_by_account_id(account_id, transaction_status)
        logger.info(f"Retrieved {len(transactions)} transactions for account {account_id}")
        
        return list[TransactionBase](
            TransactionBase(    
                id=t.id,
                amount=t.amount,
                status=t.status,
            )
            for t in transactions
        )
        
