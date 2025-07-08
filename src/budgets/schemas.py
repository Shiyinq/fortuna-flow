from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, model_validator
from typing import Literal, Optional

class BudgetBase(BaseModel):
    budgetId: UUID = Field(default_factory=lambda: str(uuid4()))
    userId: UUID = Field(default=None)
    walletId: UUID = Field(default=None)
    name: str = Field(max_length=50)
    amount: int = Field(gt=0)
    categoryId: UUID = Field(default=None)
    type: Literal['this_month', 'this_week', 'custom']
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Monthly Groceries",
                "amount": 2000000,
                "categoryId": "uuid-category",
                "walletId": "uuid-wallet",
                "type": "month"
            }
        }

class BudgetCreate(BudgetBase):
    @model_validator(mode='after')
    def validate_custom_dates(self):
        if self.type == 'custom' and (not self.startDate or not self.endDate):
            raise ValueError('startDate dan endDate wajib diisi jika type custom')
        return self

    def to_dict(self):
        data = self.dict()
        data["budgetId"] = str(self.budgetId)
        data["userId"] = str(self.userId) if self.userId else None
        data["walletId"] = str(self.walletId) if self.walletId else None
        data["categoryId"] = str(self.categoryId) if self.categoryId else None
        return data

class BudgetUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[int] = None
    categoryId: Optional[UUID] = None
    walletId: Optional[UUID] = None
    type: Optional[Literal['month', 'this_week', 'custom']] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    updatedAt: datetime = Field(default_factory=datetime.now)

    @model_validator(mode='after')
    def validate_custom_dates(self):
        if self.type == 'custom' and (not self.startDate or not self.endDate):
            raise ValueError('startDate dan endDate wajib diisi jika type custom')
        return self

    def to_dict(self):
        data = self.dict(exclude_unset=True)
        if "categoryId" in data and data["categoryId"] is not None:
            data["categoryId"] = str(data["categoryId"])
        if "walletId" in data and data["walletId"] is not None:
            data["walletId"] = str(data["walletId"])
        if "userId" in data and data["userId"] is not None:
            data["userId"] = str(data["userId"])
        if "budgetId" in data and data["budgetId"] is not None:
            data["budgetId"] = str(data["budgetId"])
        return data

class BudgetResponse(BaseModel):
    detail: str 