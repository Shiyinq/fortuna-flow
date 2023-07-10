from datetime import datetime
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class TransactionBase(BaseModel):
    transactionId: UUID = Field(default_factory=lambda: str(uuid4()))
    walletId: UUID = Field(default=None)
    categoryId: UUID = Field(default=None)
    userId: UUID = Field(default=None)
    amount: int = Field(gt=0)
    type: Literal["expense", "income"]
    note: str = Field(max_length=255, default=None)
    transactionDate: str
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)

    class Config:
        schema_extra = {
            "walletId": UUID,
            "categoryId": UUID,
            "amount": 10000,
            "type": "expense",
            "note": "Food & Drink",
            "transactionDate": "2023-07-10",
        }


class TransactionCreate(TransactionBase):
    def to_dict(self):
        data = self.dict()
        data["walletId"] = self.walletId.hex
        data["categoryId"] = self.categoryId.hex
        return data


class TransactionCreateResponse(BaseModel):
    detail: str
