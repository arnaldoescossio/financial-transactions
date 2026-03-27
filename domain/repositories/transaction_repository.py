from typing import override

from sqlalchemy.orm import Session

from domain.entities.transaction import TransactionCreate
from domain.enums.transaction_status import TransactionStatus
from domain.repositories.base_repository import Repository
from infrastructure.models.transaction_model import TransactionModel

class TransactionRepository(Repository[TransactionModel]):   
    
    @override
    def get_all(self) -> list[TransactionModel]:
        models = self._db.query(TransactionModel).all()
        return models
    
    @override
    def save(self, transaction: TransactionCreate) -> TransactionModel:
        model = TransactionModel(
            amount=transaction.amount,
            status=transaction.status.value,
            account_id=transaction.account_id
        )
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return model

    def get_by_account_id(self, account_id: int, transaction_status: TransactionStatus = TransactionStatus.SUCCESS) -> list[TransactionModel]:
        """ Retrieve transactions by account ID and optional status. 
            If status is not provided, it defaults to TransactionStatus.SUCCESS.
        
        Args:
            account_id (int): The ID of the account to retrieve transactions for.
            transaction_status (TransactionStatus, optional): Filter transactions by status. Defaults to TransactionStatus.SUCCESS.
        
        Returns:
            list[TransactionModel]: A list of transactions matching the criteria.
        """
        
        query = self._db.query(TransactionModel.id, TransactionModel.amount, TransactionModel.status).filter(
            TransactionModel.account_id == account_id,
            TransactionModel.status == transaction_status.value
        )
        
        return query.all()