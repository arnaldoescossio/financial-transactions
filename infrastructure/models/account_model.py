from datetime import datetime
from unicodedata import decimal
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Float, DateTime, func

from infrastructure.database import Base


class AccountModel(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    balance: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    