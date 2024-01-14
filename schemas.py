from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ItemStatus(Enum):
    ON_SALE = "ON_SALE"
    SOLD_OUT = "SOLD OUT"


class ItemCreate(BaseModel):
    name: str = Field(min_length=2, max_length=20, examples=["PC"])
    price: int = Field(gt=0, examples=[10000])
    description: Optional[str] = Field(None, examples=["美品"])


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=20, examples=["PC"])
    price: Optional[int] = Field(None, gt=0, examples=[10000])
    description: Optional[str] = Field(None, examples=["美品"])
    status: Optional[ItemStatus] = Field(None, examples=[ItemStatus.SOLD_OUT])


class ItemResponse(BaseModel):
    id: int = Field(gt=0, examples=[1])
    name: str = Field(min_length=2, max_length=20, examples=["PC"])
    price: int = Field(gt=0, examples=[10000])
    description: Optional[str] = Field(None, examples=["美品"])
    status: ItemStatus = Field(examples=[ItemStatus.ON_SALE])
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )  # PydanticのスキーマがORMモデル（つまりmodels.pyに定義したモデル）のオブジェクトを受け取り自動的にレスポンススキーマに変換させるための設定


class UserCreate(BaseModel):
    username: str = Field(min_length=2, examples=["user1"])
    password: str = Field(min_length=8, examples=["test1234"])


class UserResponse(BaseModel):
    id: int = Field(gp=0, examples=[1])
    username: str = Field(min_length=2, examples=["user1"])
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class DecodedToken(BaseModel):
    username: str
    user_id: int
