from typing import List, Optional

from pydantic import BaseModel, RootModel


class TransactionData(BaseModel):
    income: List[int]
    expense: List[int]


class TotalTransactions(BaseModel):
    month: List[str]
    data: TransactionData


class ActivityTransactionItem(BaseModel):
    date: str
    value: int
    amount: int


class ActivityGroup(BaseModel):
    startDate: str
    endDate: str
    totalAmount: int
    totalCount: int
    transactions: List[ActivityTransactionItem]


class ActivitiesResponse(List[ActivityGroup]):
    pass
