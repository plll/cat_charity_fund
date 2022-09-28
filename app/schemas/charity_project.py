from datetime import datetime, timedelta
from typing import Optional, Union

from pydantic import BaseModel, Field, Extra, PositiveInt


class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount : PositiveInt

    class Config:
        extra = Extra.forbid


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount : Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount : int
    fully_invested : bool
    create_date : datetime
    close_date: Optional[datetime] 

    class Config:
        orm_mode = True