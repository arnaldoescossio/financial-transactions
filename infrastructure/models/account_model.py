from datetime import datetime
from typing import Literal
from typing_extensions import Literal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Float, DateTime, String, func

from infrastructure.database import Base


class AccountModel(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    balance: Mapped[float] = mapped_column(Float, nullable=False)
    type: Mapped[Literal["checking", "savings"]] = mapped_column(String(20), default="checking")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    transactions = relationship("TransactionModel", back_populates="account")
    