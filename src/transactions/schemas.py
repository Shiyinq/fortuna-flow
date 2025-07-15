from datetime import datetime
from typing import Literal, Any, Dict, List, Optional
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
        json_schema_extra = {
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
        json_schema_extra = {
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


class RecentTransactionItem(BaseModel):
    transactionId: str
    walletId: str
    categoryId: str
    amount: int
    type: str
    note: Optional[str]
    transactionDate: str
    categoryIcon: Optional[str]
    categoryName: Optional[str]


class RecentTransactionsResponse(BaseModel):
    transactions: List[RecentTransactionItem]


class CategoryDetail(BaseModel):
    categoryIcon: Optional[str]
    name: Optional[str]
    type: Optional[str]


class TransactionItem(BaseModel):
    transactionId: str
    walletId: str
    categoryId: str
    categoryDetail: CategoryDetail
    amount: int
    type: str
    note: Optional[str]
    createdAt: datetime
    updatedAt: datetime


class TransactionsGroup(BaseModel):
    totalAmountExpense: int
    totalAmountIncome: int
    transactions: List[TransactionItem]
    transactionDate: str


class TransactionsMetadata(BaseModel):
    totalData: int
    totalPage: int
    previousPage: Optional[int]
    currentPage: int
    nextPage: Optional[int]


class TransactionsResponse(BaseModel):
    metadata: TransactionsMetadata
    data: List[TransactionsGroup]
