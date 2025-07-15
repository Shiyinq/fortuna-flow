from datetime import datetime
from typing import Literal, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    categoryId: UUID = Field(default_factory=lambda: str(uuid4()))
    userId: UUID = Field(default=None)
    categoryIcon: str | None = Field(max_length=20, default=None)
    name: str = Field(max_length=20)
    type: Literal["expense", "income"]
    createdAt: datetime = Field(default_factory=datetime.now, example=None)
    updatedAt: datetime = Field(default_factory=datetime.now, example=None)

    class Config:
        json_schema_extra = {"example": {"name": "Transportation", "type": "expense"}}


class CategoryCreate(CategoryBase):
    pass


class CategoryCreateResponse(BaseModel):
    detail: str


class CategoryItem(BaseModel):
    categoryId: str
    userId: str
    categoryIcon: Optional[str]
    name: str
    type: str
    createdAt: datetime
    updatedAt: datetime


class CategoriesMetadata(BaseModel):
    page: int
    limit: int
    prevPage: Optional[int]
    nextPage: Optional[int]
    totalPage: int


class CategoriesResponse(BaseModel):
    metadata: CategoriesMetadata
    data: List[CategoryItem]
