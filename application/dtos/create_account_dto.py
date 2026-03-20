
from decimal import Decimal

from application.dtos.base_dto import Dto
from domain.entities.account import Account, AccountCreate, AccountCreate


class CreateAccountDTO(Dto):
    balance: float

    def __init__(self, balance: float):
        if balance < 0:
             raise ValueError("balance cannot be negative")
        self.balance = balance

    def to_entity(self) -> Account:
        return Account(
            id=None,
            balance=self.balance
        )
    
    @staticmethod
    def from_entity(entity: AccountCreate) -> 'CreateAccountDTO':
        return CreateAccountDTO(
            balance=entity.balance
        )