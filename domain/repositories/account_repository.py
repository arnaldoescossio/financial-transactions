from abc import abstractmethod

from domain.entities.account import Account, AccountResponse
from domain.enums.transaction_status import TransactionStatus
from domain.repositories.base_repository import Repository
from infrastructure.models.account_model import AccountModel

class AccountRepository(Repository):
    """Repository for managing account data."""
    
    @abstractmethod
    def save(self, account) -> Account:
        """Create a new account in the repository."""
        model = AccountModel(
            balance=account.balance,
            type=account.type
        )
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return self._to_entity(model)
        # Implementation to save the account to the database or in-memory storage
        
    
    @abstractmethod
    def get_by_id(self, account_id) -> Account:
        """Retrieve an account by its ID."""
        # Implementation to retrieve the account from the database or in-memory storage
        pass
    
    @abstractmethod
    def update(self, account):
        """Update an existing account in the repository."""
        # Implementation to update the account in the database or in-memory storage
        pass
    
    @abstractmethod
    def delete(self, account_id):
        """Delete an account by its ID."""
        # Implementation to delete the account from the database or in-memory storage
        pass

    def _to_entity(self, model: AccountModel) -> AccountResponse:
        return AccountResponse(
            id=model.id,
            balance=model.balance,
            type=model.type,
            transactions=[]  # Placeholder for transactions, can be populated with actual data if needed
        )