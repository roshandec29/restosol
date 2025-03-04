from pydantic import BaseModel
from datetime import datetime


class DiscountApplyRequest(BaseModel):
    order_id: int
    discount_code: str


class DiscountResponse(BaseModel):
    code: str
    discount_type: str
    value: float
    valid_until: datetime
