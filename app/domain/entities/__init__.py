"""Domain entities."""

# Import all entities first
from app.domain.entities.account import Account
from app.domain.entities.transaction import Transaction
from app.domain.entities.user import User

# Rebuild models to resolve forward references
Account.model_rebuild()
Transaction.model_rebuild()
User.model_rebuild()

__all__ = ["Account", "Transaction", "User"]
