from typing import List
from pydantic import BaseModel

class TransactionData(BaseModel):
    income: List[int]
    expense: List[int]

class TotalTransactions(BaseModel):
    month: List[str]
    data: TransactionData
