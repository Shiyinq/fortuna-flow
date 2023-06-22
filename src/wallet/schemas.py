from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field 


class WalletBase(BaseModel):
    walletId: UUID = Field(default_factory=lambda: str(uuid4()))
    userId: str = None
    name: str
    balance: int
    createdAt: datetime = Field(default_factory=datetime.now, example=None)
    updatedAt: datetime = Field(default_factory=datetime.now, example=None)

    class Config:
        schema_extra = {
            "example": {
                "name": "My wallet",
                "balance": 1000000000
            }
        }

class WalletCreate(WalletBase):
    def to_dict(self):
        data = self.dict()
        data["walletId"] = self.walletId.hex

        return data

class WalletCreateResponse(BaseModel):
    detail: str
