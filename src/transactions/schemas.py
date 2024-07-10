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
            "example": {
                "walletId": uuid4(),
                "categoryId": uuid4(),
                "amount": 10000,
                "type": "expense",
                "note": "Food & Drink",
                "transactionDate": "2023-07-10",
            }
        }


class TransactionCreate(TransactionBase):
    def to_dict(self):
        data = self.dict()
        data["walletId"] = str(self.walletId)
        data["categoryId"] = str(self.categoryId)
        return data


class TransactionUpdate(TransactionBase):
    def to_dict(self):
        data = self.dict()
        data["categoryId"] = str(self.categoryId)
        return {k: v for k, v in data.items() if v is not None}

    class Config:
        fields = {
            "transactionId": {"exclude": True},
            "walletId": {"exclude": True},
            "userId": {"exclude": True},
            "transactionId": {"exclude": True},
            "createdAt": {"exclude": True},
        }
        schema_extra = {
            "example": {
                "categoryId": uuid4(),
                "amount": 10000,
                "type": "expense",
                "note": "Food & Drink",
                "transactionDate": "2023-07-10",
            }
        }


class TransactionCreateResponse(BaseModel):
    detail: str
