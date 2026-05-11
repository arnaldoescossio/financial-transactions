from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class AccountBase(BaseModel):
    id: int | None = None
    balance: float = Field(ge=0.00)
    type: Literal["checking", "savings"] = Field(default="checking")


class AccountCreate(AccountBase):
    pass


class AccountResponse(AccountBase):
    model_config = ConfigDict(from_attributes=True)

    transactions: list | None = None
