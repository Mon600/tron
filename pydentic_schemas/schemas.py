from datetime import datetime
from decimal import Decimal
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator


class InfoSchema(BaseModel):
    address: str
    balance: float
    bandwidth: int
    energy: int


class HistorySchema(BaseModel):
    id: int
    address: str
    date: datetime

    model_config = ConfigDict(from_attributes=True)


class AddressRequest(BaseModel):
    address: str = Field(min_length=32)


    @field_validator("address", mode='before')
    def validate(cls, value: str):
        if value[0] != "T":
            raise ValueError("Этот адрес не находится в сети Tron")
        return value