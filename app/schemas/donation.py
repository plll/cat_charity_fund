from datetime import datetime, timedelta
from typing import Optional, Union

from pydantic import BaseModel, Field, Extra, PositiveInt


class DonationCreate(BaseModel):
    comment: Optional[str]
    full_amount : PositiveInt
    user_id : Optional[int]
    
    class Config:
        extra = Extra.forbid


class DonationDB(DonationCreate):
    id: int
    invested_amount : int
    fully_invested : bool = False
    create_date : datetime
    close_date : Union[datetime, None] 

    class Config:
        orm_mode = True