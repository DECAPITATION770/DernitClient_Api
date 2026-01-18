from pydantic import BaseModel, Field
from typing import Optional
import time

class PriceResponse(BaseModel):
    id: int
    ticker: str
    price: float
    timestamp: int

    class Config:
        from_attributes = True


class PriceFilter(BaseModel):
    ticker: str
    date_from: Optional[int] = Field(time.time(), description="Unix timestamp")
    date_to: Optional[int] = Field(time.time(), description="Unix timestamp")