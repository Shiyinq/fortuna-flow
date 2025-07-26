from datetime import datetime

from pydantic import BaseModel, Field


class CreateAPIKey(BaseModel):
    userId: str
    hashKey: str 
    createdAt: datetime = Field(default_factory=datetime.now, example=None)
    lastUsedAt: datetime = Field(default_factory=datetime.now, example=None)


class APIKeysResponse(BaseModel):
    detail: str
    apiKey: str